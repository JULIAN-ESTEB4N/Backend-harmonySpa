from enum import Enum

class UserRoles(str , Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    ESTETICISTA = "ESTETICISTA"
    CLIENTE = "CLIENTE"