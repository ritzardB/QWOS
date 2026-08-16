from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from qwos.core.database.repositories.base_repository import BaseRepository
from qwos.domains.hr.models.employee_reporting_relationship import (
    EmployeeReportingRelationship,
)
from qwos.domains.hr.repositories.employee_reporting_relationship_repository import (
    EmployeeReportingRelationshipRepository,
)


class SQLAlchemyEmployeeReportingRelationshipRepository(
    BaseRepository[EmployeeReportingRelationship],
    EmployeeReportingRelationshipRepository,
):
    """
    SQLAlchemy implementation of EmployeeReportingRelationshipRepository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(
            session=session,
            model=EmployeeReportingRelationship,
        )

    def get_active_primary_manager(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> EmployeeReportingRelationship | None:
        stmt = select(EmployeeReportingRelationship).where(
            EmployeeReportingRelationship.tenant_id == tenant_id,
            EmployeeReportingRelationship.employee_id == employee_id,
            EmployeeReportingRelationship.relationship_type
            == "primary_manager",
            EmployeeReportingRelationship.is_primary.is_(True),
            EmployeeReportingRelationship.deleted_at.is_(None),
            EmployeeReportingRelationship.effective_to.is_(None),
        )

        return self._session.scalar(stmt)

    def exists_active_primary_manager(
        self,
        *,
        tenant_id: str,
        employee_id: str,
    ) -> bool:
        return (
            self.get_active_primary_manager(
                tenant_id=tenant_id,
                employee_id=employee_id,
            )
            is not None
        )

    def get_active_reports(
        self,
        *,
        tenant_id: str,
        manager_employee_id: str,
    ) -> list[EmployeeReportingRelationship]:
        stmt = select(EmployeeReportingRelationship).where(
            EmployeeReportingRelationship.tenant_id == tenant_id,
            EmployeeReportingRelationship.manager_employee_id
            == manager_employee_id,
            EmployeeReportingRelationship.deleted_at.is_(None),
            EmployeeReportingRelationship.effective_to.is_(None),
        )

        return list(self._session.scalars(stmt).all())