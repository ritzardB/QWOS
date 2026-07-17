from enum import StrEnum


class UserType(StrEnum):

    SYSTEM = "SYSTEM"

    EMPLOYEE = "EMPLOYEE"

    CONTRACTOR = "CONTRACTOR"

    CUSTOMER = "CUSTOMER"

    VENDOR = "VENDOR"