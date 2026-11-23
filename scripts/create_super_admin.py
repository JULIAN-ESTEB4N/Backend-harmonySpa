import getpass
import bcrypt
from sqlalchemy import select

from app.domain.enums.user_role_ import UserRole
from app.infrastructure.database.session import SessionLocal
from app.models.user import User


def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


def create_super_admin() -> None:
    db = SessionLocal()
    try:
        existing = db.execute(
            select(User).where(User.role == UserRole.SUPER_ADMIN)
        ).scalar_one_or_none()

        if existing:
            print(f"Ya existe un SUPER_ADMIN registrado: {existing.email} (ID: {existing.id})")
            return

        print("--- Creación de SUPER_ADMIN para Harmony Spa ---")
        first_name = input("Nombre: ").strip()
        last_name = input("Apellido: ").strip()
        email = input("Correo electrónico: ").strip().lower()
        phone = input("Teléfono (opcional, Enter para omitir): ").strip() or None
        password = getpass.getpass("Contraseña (no se verá al escribir): ").strip()

        if not first_name or not last_name or not email or not password:
            print("Error: Nombre, apellido, correo y contraseña son obligatorios.")
            return

        super_admin = User(
            fisrt_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password_hash=hash_password(password),
            role=UserRole.SUPER_ADMIN,
            is_active=True,
        )

        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)
        print(f"SUPER_ADMIN creado exitosamente -> ID: {super_admin.id} | Email: {super_admin.email}")
    except Exception as e:
        db.rollback()
        print(f"Error al crear el SUPER_ADMIN: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_super_admin()