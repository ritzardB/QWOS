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
    get_authorization_service,
    get_user_profile_repository,
    get_user_repository,
)
from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.application.common.ports.document_filename_generator import (
    DocumentFilenameGenerator,
)
from qwos.application.common.ports.document_storage import (
    DocumentStorage,
)
from qwos.application.common.ports.document_storage_key_generator import (
    DocumentStorageKeyGenerator,
)
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
from qwos.application.hr.use_cases.get_employee_immigration_use_case import (
    GetEmployeeImmigrationUseCase,
)
from qwos.application.hr.use_cases.get_employee_manager_use_case import (
    GetEmployeeManagerUseCase,
)
from qwos.application.hr.use_cases.get_employee_position_use_case import (
    GetEmployeePositionUseCase,
)
from qwos.application.hr.use_cases.get_employee_profile_use_case import (
    GetEmployeeProfileUseCase,
)
from qwos.application.hr.use_cases.get_employee_use_case import (
    GetEmployeeUseCase,
)
from qwos.application.hr.use_cases.link_employee_to_user_use_case import (
    LinkEmployeeToUserUseCase,
)
from qwos.application.hr.use_cases.list_employee_immigration_use_case import (
    ListEmployeeImmigrationUseCase,
)
from qwos.application.hr.use_cases.list_employees_use_case import (
    ListEmployeesUseCase,
)
from qwos.application.hr.use_cases.list_expiring_employee_immigration_use_case import (
    ListExpiringEmployeeImmigrationUseCase,
)
from qwos.application.hr.use_cases.update_employee_profile_use_case import (
    UpdateEmployeeProfileUseCase,
)
from qwos.application.hr.use_cases.upload_employee_document_use_case import (
    UploadEmployeeDocumentUseCase,
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
from qwos.domains.hr.repositories.employee_document_repository import (
    EmployeeDocumentRepository,
)
from qwos.domains.hr.repositories.employee_immigration_repository import (
    EmployeeImmigrationRepository,
)
from qwos.domains.hr.repositories.employee_number_sequence_repository import (
    EmployeeNumberSequenceRepository,
)
from qwos.domains.hr.repositories.employee_position_repository import (
    EmployeePositionRepository,
)
from qwos.domains.hr.repositories.employee_profile_repository import (
    EmployeeProfileRepository,
)
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
from qwos.domains.identity.services.authorization_service import (
    AuthorizationService,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_document_repository import (
    SQLAlchemyEmployeeDocumentRepository,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_immigration_repository import (
    SQLAlchemyEmployeeImmigrationRepository,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_number_generator import (
    SQLAlchemyEmployeeNumberGenerator,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_number_sequence_repository import (
    SQLAlchemyEmployeeNumberSequenceRepository,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_position_repository import (
    SQLAlchemyEmployeePositionRepository,
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
from qwos.infrastructure.storage.document_filename_generator import (
    QWOSDocumentFilenameGenerator,
)
from qwos.infrastructure.storage.document_storage_key_generator import (
    QWOSDocumentStorageKeyGenerator,
)
from qwos.infrastructure.storage.local_document_storage import (
    LocalDocumentStorage,
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

def get_employee_profile_repository(
    session: Session = Depends(get_session),
) -> EmployeeProfileRepository:
    """
    Return EmployeeProfile repository.
    """
    return SQLAlchemyEmployeeProfileRepository(session)

def get_employee_reporting_relationship_repository(
    session: Session = Depends(get_session),
) -> EmployeeReportingRelationshipRepository:
    """
    Return EmployeeReportingRelationship repository.
    """
    return SQLAlchemyEmployeeReportingRelationshipRepository(session)

def get_employee_number_sequence_repository(
    session: Session = Depends(get_session),
) -> EmployeeNumberSequenceRepository:
    """
    Return Employee Number Sequence repository.
    """
    return SQLAlchemyEmployeeNumberSequenceRepository(session)

def get_employee_position_repository(
    session: Session = Depends(get_session),
) -> EmployeePositionRepository:
    """
    Return EmployeePosition repository.
    """
    return SQLAlchemyEmployeePositionRepository(session)

def get_employee_immigration_repository(
    session: Session = Depends(get_session),
) -> EmployeeImmigrationRepository:
    """
    Return EmployeeImmigration repository.
    """
    return SQLAlchemyEmployeeImmigrationRepository(session)

def get_update_employee_profile_use_case(
    employee_repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
    employee_profile_repository: EmployeeProfileRepository = Depends(
        get_employee_profile_repository,
    ),
    authorization_service=Depends(
        get_authorization_service,
    ),
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
    request_context: RequestContext = Depends(
        get_request_context,
    ),
) -> UpdateEmployeeProfileUseCase:
    """
    Return UpdateEmployeeProfileUseCase.
    """
    return UpdateEmployeeProfileUseCase(
        employee_repository=employee_repository,
        employee_profile_repository=employee_profile_repository,
        authorization_service=authorization_service,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )

def get_employee_document_repository(
    session: Session = Depends(get_session),
) -> EmployeeDocumentRepository:
    """
    Return EmployeeDocument repository.
    """
    return SQLAlchemyEmployeeDocumentRepository(session)

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


def get_create_employee_profile_validator() -> CreateEmployeeProfileValidator:
    """
    Return CreateEmployeeProfileValidator.
    """
    return CreateEmployeeProfileValidator()


def get_create_employee_reporting_relationship_validator(
) -> CreateEmployeeReportingRelationshipValidator:
    """
    Return CreateEmployeeReportingRelationshipValidator.
    """
    return CreateEmployeeReportingRelationshipValidator()


# -------------------------------------------------------------------------
# Employee Use Case Providers
# -------------------------------------------------------------------------

def get_get_employee_use_case(
    employee_repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
) -> GetEmployeeUseCase:
    """
    Return GetEmployeeUseCase.
    """
    return GetEmployeeUseCase(
        employee_repository=employee_repository,
    )

def get_list_employees_use_case(
    employee_repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
    request_context: RequestContext = Depends(
        get_request_context,
    ),
) -> ListEmployeesUseCase:
    """
    Return ListEmployeesUseCase.
    """
    return ListEmployeesUseCase(
        employee_repository=employee_repository,
        request_context=request_context,
    )

def get_get_employee_position_use_case(
    employee_position_repository: EmployeePositionRepository = Depends(
        get_employee_position_repository,
    ),
) -> GetEmployeePositionUseCase:
    """
    Return GetEmployeePositionUseCase.
    """
    return GetEmployeePositionUseCase(
        employee_position_repository=employee_position_repository,
    )

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

def get_document_filename_generator() -> DocumentFilenameGenerator:
    """
    Return the QWOS document filename generator.
    """
    return QWOSDocumentFilenameGenerator()


def get_document_storage_key_generator() -> DocumentStorageKeyGenerator:
    """
    Return the QWOS document storage-key generator.
    """
    return QWOSDocumentStorageKeyGenerator()


def get_document_storage() -> DocumentStorage:
    """
    Return the configured document storage provider.
    """
    from qwos.core.config.settings import settings

    if settings.DOCUMENT_STORAGE_PROVIDER != "local":
        raise RuntimeError(
            "Unsupported document storage provider: "
            f"{settings.DOCUMENT_STORAGE_PROVIDER}"
        )

    return LocalDocumentStorage(
        root_path=settings.DOCUMENT_STORAGE_ROOT,
    )

def get_upload_employee_document_use_case(
    employee_repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
    employee_immigration_repository: EmployeeImmigrationRepository = Depends(
        get_employee_immigration_repository,
    ),
    employee_document_repository: EmployeeDocumentRepository = Depends(
        get_employee_document_repository,
    ),
    authorization_service: AuthorizationService = Depends(
        get_authorization_service,
    ),
    filename_generator: DocumentFilenameGenerator = Depends(
        get_document_filename_generator,
    ),
    storage_key_generator: DocumentStorageKeyGenerator = Depends(
        get_document_storage_key_generator,
    ),
    document_storage: DocumentStorage = Depends(
        get_document_storage,
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
) -> UploadEmployeeDocumentUseCase:
    """
    Return UploadEmployeeDocumentUseCase.
    """
    return UploadEmployeeDocumentUseCase(
        employee_repository=employee_repository,
        employee_immigration_repository=employee_immigration_repository,
        employee_document_repository=employee_document_repository,
        authorization_service=authorization_service,
        filename_generator=filename_generator,
        storage_key_generator=storage_key_generator,
        document_storage=document_storage,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        request_context=request_context,
    )
authorization_service: AuthorizationService = Depends(
    get_authorization_service,
),

# -------------------------------------------------------------------------
# Employee Profile Providers
# -------------------------------------------------------------------------

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

def get_get_employee_profile_use_case(
    employee_profile_repository: EmployeeProfileRepository = Depends(
        get_employee_profile_repository,
    ),
) -> GetEmployeeProfileUseCase:
    """
    Return GetEmployeeProfileUseCase.
    """
    return GetEmployeeProfileUseCase(
        employee_profile_repository=employee_profile_repository,
    )

# -------------------------------------------------------------------------
# Employee ↔ User Providers
# -------------------------------------------------------------------------

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

# -------------------------------------------------------------------------
# Employee Reporting Relationship Providers
# -------------------------------------------------------------------------

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
    """
    Return CreateEmployeeReportingRelationshipUseCase.
    """
    return CreateEmployeeReportingRelationshipUseCase(
        employee_repository=employee_repository,
        relationship_repository=relationship_repository,
        id_generator=id_generator,
        unit_of_work=unit_of_work,
        validator=validator,
        request_context=request_context,
    )

def get_get_employee_manager_use_case(
    employee_repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
    relationship_repository: EmployeeReportingRelationshipRepository = Depends(
        get_employee_reporting_relationship_repository,
    ),
) -> GetEmployeeManagerUseCase:
    """
    Return GetEmployeeManagerUseCase.
    """
    return GetEmployeeManagerUseCase(
        employee_repository=employee_repository,
        relationship_repository=relationship_repository,
    )

# -------------------------------------------------------------------------
# Employee Immigration Providers
# ------------------------------------------------------------------------- 

def get_get_employee_immigration_use_case(
    employee_immigration_repository: EmployeeImmigrationRepository = Depends(
        get_employee_immigration_repository,
    ),
) -> GetEmployeeImmigrationUseCase:
    """
    Return GetEmployeeImmigrationUseCase.
    """
    return GetEmployeeImmigrationUseCase(
        employee_immigration_repository=employee_immigration_repository,
    )


def get_list_employee_immigration_use_case(
    employee_immigration_repository: EmployeeImmigrationRepository = Depends(
        get_employee_immigration_repository,
    ),
) -> ListEmployeeImmigrationUseCase:
    """
    Return ListEmployeeImmigrationUseCase.
    """
    return ListEmployeeImmigrationUseCase(
        employee_immigration_repository=employee_immigration_repository,
    )


def get_list_expiring_employee_immigration_use_case(
    employee_immigration_repository: EmployeeImmigrationRepository = Depends(
        get_employee_immigration_repository,
    ),
) -> ListExpiringEmployeeImmigrationUseCase:
    """
    Return ListExpiringEmployeeImmigrationUseCase.
    """
    return ListExpiringEmployeeImmigrationUseCase(
        employee_immigration_repository=employee_immigration_repository,
    )

# -------------------------------------------------------------------------
# Employee Storage Providers
# ------------------------------------------------------------------------- 


def get_document_filename_generator() -> DocumentFilenameGenerator:
    """
    Return the QWOS document filename generator.
    """
    return QWOSDocumentFilenameGenerator()


def get_document_storage_key_generator() -> DocumentStorageKeyGenerator:
    """
    Return the QWOS document storage-key generator.
    """
    return QWOSDocumentStorageKeyGenerator()


def get_document_storage() -> DocumentStorage:
    """
    Return the configured document storage provider.
    """
    from qwos.core.config.settings import settings

    if settings.DOCUMENT_STORAGE_PROVIDER != "local":
        raise RuntimeError(
            "Unsupported document storage provider: "
            f"{settings.DOCUMENT_STORAGE_PROVIDER}"
        )

    return LocalDocumentStorage(
        root_path=settings.DOCUMENT_STORAGE_ROOT,
    )