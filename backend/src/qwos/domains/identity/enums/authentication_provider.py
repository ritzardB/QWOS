from enum import StrEnum


class AuthenticationProvider(StrEnum):
    LOCAL = "LOCAL"

    GOOGLE = "GOOGLE"

    MICROSOFT = "MICROSOFT"

    APPLE = "APPLE"

    GITHUB = "GITHUB"

    SAML = "SAML"
