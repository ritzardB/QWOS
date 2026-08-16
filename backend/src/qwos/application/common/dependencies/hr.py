"""
===============================================================================
Quantum Workforce OS (QWOS)

Application Layer

Dependency Providers

HR Module

Description:
    Dependency providers for the HR module.

Responsibilities:
    - Provide HR repositories
    - Provide HR validators
    - Provide HR services
    - Provide HR use cases
    - Compose the HR object graph

Author:
    Richard Balabarcon
===============================================================================
"""

from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from qwos.application.common.context.request_context import RequestContext
from qwos.application.common.dependencies import (
    get_id_generator,
    get_request_context,
    get_unit_of_work,
)
from qwos.application.common.dependencies.identity import (
    get_user_profile_repository,
    get_user_repository,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.employee_number_generator import (
    EmployeeNumberGenerator,
)
from qwos.application.common.ports.id_generator import IdGenerator
from qwos.application.hr.use_cases.create_employee_profile_use_case import (
    CreateEmployeeProfileUseCase,
)
from qwos.application.hr.use_cases.create_employee_reporting_relationship_use_case import (
    CreateEmployeeReportingRelationshipUseCase,
)
from qwos.application.hr.use_cases.create_employee_use_case import (
    CreateEmployeeUseCase,
)
from qwos.application.hr.use_cases.link_employee_to_user_use_case import (
    LinkEmployeeToUserUseCase,
)
from qwos.application.hr.validators.create_employee_profile_validator import (
    CreateEmployeeProfileValidator,
)
from qwos.application.hr.validators.create_employee_reporting_relationship_validator import (
    CreateEmployeeReportingRelationshipValidator,
)
from qwos.application.hr.validators.create_employee_validator import (
    CreateEmployeeValidator,
)
from qwos.core.database.session import get_session
from qwos.domains.hr.repositories.employee_number_sequence_repository import (
    EmployeeNumberSequenceRepository,
)
from qwos.domains.hr.repositories.employee_profile_repository import EmployeeProfileRepository
from qwos.domains.hr.repositories.employee_reporting_relationship_repository import (
    EmployeeReportingRelationshipRepository,
)
from qwos.domains.hr.repositories.employee_repository import (
    EmployeeRepository,
)
from qwos.domains.identity.repositories.user_profile_repository import (
    UserProfileRepository,
)
from qwos.domains.identity.repositories.user_repository import (
    UserRepository,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_number_generator import (
    SQLAlchemyEmployeeNumberGenerator,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_number_sequence_repository import (
    SQLAlchemyEmployeeNumberSequenceRepository,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_profile_repository import (
    SQLAlchemyEmployeeProfileRepository,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_reporting_relationship_repository import (
    SQLAlchemyEmployeeReportingRelationshipRepository,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_repository import (
    SQLAlchemyEmployeeRepository,
)

# -------------------------------------------------------------------------
# Repository Providers
# -------------------------------------------------------------------------


def get_employee_repository(
    session: Session = Depends(get_session),
) -> EmployeeRepository:
    """
    Return Employee repository.
    """
    return SQLAlchemyEmployeeRepository(session)


def get_employee_number_sequence_repository(
    session: Session = Depends(get_session),
) -> EmployeeNumberSequenceRepository:
    """
    Return Employee Number Sequence repository.
    """
    return SQLAlchemyEmployeeNumberSequenceRepository(session)


# -------------------------------------------------------------------------
# HR Infrastructure Providers
# -------------------------------------------------------------------------


def get_employee_number_generator(
    repository: EmployeeNumberSequenceRepository = Depends(
        get_employee_number_sequence_repository,
    ),
) -> EmployeeNumberGenerator:
    """
    Return the tenant employee-number generator.
    """
    return SQLAlchemyEmployeeNumberGenerator(
        repository=repository,
    )


# -------------------------------------------------------------------------
# Validator Providers
# -------------------------------------------------------------------------


def get_create_employee_validator() -> CreateEmployeeValidator:
    """
    Return CreateEmployeeValidator.
    """
    return CreateEmployeeValidator()


# -------------------------------------------------------------------------
# Use Case Providers
# -------------------------------------------------------------------------


def get_create_employee_use_case(
    employee_repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
    employee_number_generator: EmployeeNumberGenerator = Depends(
        get_employee_number_generator,
    ),
    id_generator: IdGenerator = Depends(
        get_id_generator,
    ),
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
    validator: CreateEmployeeValidator = Depends(
        get_create_employee_validator,
    ),
    request_context: RequestContext = Depends(
        get_request_context,
    ),
) -> CreateEmployeeUseCase:
    """
    Return CreateEmployeeUseCase.
    """

    return CreateEmployeeUseCase(
        employee_repository=employee_repository,
        user_repository=user_repository,
        employee_number_generator=employee_number_generator,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )

# -------------------------------------------------------------------------
# Employee Profile Providers
# -------------------------------------------------------------------------

def get_employee_profile_repository(
    session: Session = Depends(get_session),
) -> EmployeeProfileRepository:
    """
    Return EmployeeProfile repository.
    """
    return SQLAlchemyEmployeeProfileRepository(session)


def get_create_employee_profile_validator() -> CreateEmployeeProfileValidator:
    """
    Return CreateEmployeeProfileValidator.
    """
    return CreateEmployeeProfileValidator()


def get_create_employee_profile_use_case(
    employee_repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
    employee_profile_repository: EmployeeProfileRepository = Depends(
        get_employee_profile_repository,
    ),
    id_generator: IdGenerator = Depends(
        get_id_generator,
    ),
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
    validator: CreateEmployeeProfileValidator = Depends(
        get_create_employee_profile_validator,
    ),
    request_context: RequestContext = Depends(
        get_request_context,
    ),
) -> CreateEmployeeProfileUseCase:
    """
    Return CreateEmployeeProfileUseCase.
    """

    return CreateEmployeeProfileUseCase(
        employee_repository=employee_repository,
        employee_profile_repository=employee_profile_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )

def get_link_employee_to_user_use_case(
    employee_repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
    user_profile_repository: UserProfileRepository = Depends(
        get_user_profile_repository,
    ),
    id_generator: IdGenerator = Depends(
        get_id_generator,
    ),
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
    request_context: RequestContext = Depends(
        get_request_context,
    ),
) -> LinkEmployeeToUserUseCase:
    """
    Return LinkEmployeeToUserUseCase.
    """

    return LinkEmployeeToUserUseCase(
        employee_repository=employee_repository,
        user_repository=user_repository,
        user_profile_repository=user_profile_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

def get_employee_reporting_relationship_repository(
    session: Session = Depends(get_session),
) -> EmployeeReportingRelationshipRepository:
    return SQLAlchemyEmployeeReportingRelationshipRepository(session)


def get_create_employee_reporting_relationship_validator(
) -> CreateEmployeeReportingRelationshipValidator:
    return CreateEmployeeReportingRelationshipValidator()


def get_create_employee_reporting_relationship_use_case(
    employee_repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
    relationship_repository: EmployeeReportingRelationshipRepository = Depends(
        get_employee_reporting_relationship_repository,
    ),
    id_generator: IdGenerator = Depends(
        get_id_generator,
    ),
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
    validator: CreateEmployeeReportingRelationshipValidator = Depends(
        get_create_employee_reporting_relationship_validator,
    ),
    request_context: RequestContext = Depends(
        get_request_context,
    ),
) -> CreateEmployeeReportingRelationshipUseCase:
    return CreateEmployeeReportingRelationshipUseCase(
        employee_repository=employee_repository,
        relationship_repository=relationship_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )