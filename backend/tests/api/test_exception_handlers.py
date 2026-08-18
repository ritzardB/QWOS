from fastapi.testclient import TestClient

from qwos.application.common.exceptions.account_locked_exception import (
    AccountLockedException,
)
from qwos.application.common.exceptions.application_exception import (
    ApplicationException,
)
from qwos.application.common.exceptions.duplicate_resource_exception import (
    DuplicateResourceException,
)
from qwos.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from qwos.application.common.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from qwos.application.common.exceptions.resource_not_found_exception import (
    ResourceNotFoundException,
)
from qwos.application.common.exceptions.validation_exception import (
    ValidationException,
)
from qwos.application.common.results.validation_result import ValidationResult
from qwos.main import app


@app.get("/test/application-exception")
def raise_application_exception() -> None:
    raise ApplicationException("Test application error.")


@app.get("/test/invalid-credentials")
def raise_invalid_credentials() -> None:
    raise InvalidCredentialsException()


@app.get("/test/account-locked")
def raise_account_locked() -> None:
    raise AccountLockedException()


@app.get("/test/duplicate-resource")
def raise_duplicate_resource() -> None:
    raise DuplicateResourceException(
        resource="User",
        field="email",
        value="test@example.com",
    )


@app.get("/test/resource-not-found")
def raise_resource_not_found() -> None:
    raise ResourceNotFoundException(
        resource="User",
        identifier="01TEST",
    )


@app.get("/test/validation")
def raise_validation() -> None:
    raise ValidationException(
        ValidationResult(),
    )

@app.get("/test/forbidden")
def raise_forbidden() -> None:
    raise ForbiddenException(
        message="Test forbidden error.",
    )

def test_application_exception_returns_400() -> None:
    client = TestClient(app)

    response = client.get("/test/application-exception")

    assert response.status_code == 400

    body = response.json()

    assert body["success"] is False
    assert body["message"] == "Test application error."
    assert body["errors"][0]["code"] == "ApplicationException"


def test_invalid_credentials_returns_401() -> None:
    client = TestClient(app)

    response = client.get("/test/invalid-credentials")

    assert response.status_code == 401

    body = response.json()

    assert body["success"] is False
    assert body["errors"][0]["code"] == "InvalidCredentialsException"


def test_account_locked_returns_423() -> None:
    client = TestClient(app)

    response = client.get("/test/account-locked")

    assert response.status_code == 423

    body = response.json()

    assert body["success"] is False
    assert body["errors"][0]["code"] == "AccountLockedException"


def test_duplicate_resource_returns_409() -> None:
    client = TestClient(app)

    response = client.get("/test/duplicate-resource")

    assert response.status_code == 409

    body = response.json()

    assert body["success"] is False
    assert body["errors"][0]["code"] == "DuplicateResourceException"


def test_resource_not_found_returns_404() -> None:
    client = TestClient(app)

    response = client.get("/test/resource-not-found")

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["errors"][0]["code"] == "ResourceNotFoundException"


def test_validation_exception_returns_400() -> None:
    client = TestClient(app)

    response = client.get("/test/validation")

    assert response.status_code == 400

    body = response.json()

    assert body["success"] is False
    assert body["errors"][0]["code"] == "ValidationException"

def test_forbidden_returns_403() -> None:
    client = TestClient(app)

    response = client.get("/test/forbidden")

    assert response.status_code == 403

    body = response.json()

    assert body["success"] is False
    assert body["message"] == "Test forbidden error."
    assert body["errors"][0]["code"] == "ForbiddenException"
    assert body["errors"][0]["message"] == "Test forbidden error."

