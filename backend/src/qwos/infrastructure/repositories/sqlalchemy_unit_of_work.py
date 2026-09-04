from __future__ import annotations

from types import TracebackType

from sqlalchemy.orm import Session

from qwos.application.common.persistence.unit_of_work import UnitOfWork
from qwos.infrastructure.repositories.attendance.sqlalchemy_attendance_event_repository import (
    SQLAlchemyAttendanceEventRepository,
)
from qwos.infrastructure.repositories.attendance.sqlalchemy_attendance_record_repository import (
    SQLAlchemyAttendanceRecordRepository,
)
from qwos.infrastructure.repositories.attendance.sqlalchemy_employee_work_arrangement_repository import (
    SQLAlchemyEmployeeWorkArrangementRepository,
)
from qwos.infrastructure.repositories.attendance.sqlalchemy_employee_work_schedule_repository import (
    SQLAlchemyEmployeeWorkScheduleRepository,
)
from qwos.infrastructure.repositories.attendance.sqlalchemy_work_schedule_day_repository import (
    SQLAlchemyWorkScheduleDayRepository,
)
from qwos.infrastructure.repositories.attendance.sqlalchemy_work_schedule_repository import (
    SQLAlchemyWorkScheduleRepository,
)
from qwos.infrastructure.repositories.hr.sqlalchemy_employee_repository import (
    SQLAlchemyEmployeeRepository,
)
from qwos.infrastructure.repositories.leave.sqlalchemy_leave_type_repository import (
    SQLAlchemyLeaveTypeRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    """
    SQLAlchemy implementation of UnitOfWork.

    Owns the SQLAlchemy session and all repositories participating
    in the same transaction.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

        # -----------------------------------------------------------------
        # HR repositories
        # -----------------------------------------------------------------

        self.employee_repository = SQLAlchemyEmployeeRepository(
            session,
        )

        # -----------------------------------------------------------------
        # Attendance repositories
        # -----------------------------------------------------------------

        self.attendance_record_repository = (
            SQLAlchemyAttendanceRecordRepository(session)
        )

        self.attendance_event_repository = (
            SQLAlchemyAttendanceEventRepository(session)
        )

        self.employee_work_arrangement_repository = (
            SQLAlchemyEmployeeWorkArrangementRepository(session)
        )

        self.employee_work_schedule_repository = (
            SQLAlchemyEmployeeWorkScheduleRepository(session)
        )

        self.work_schedule_repository = (
            SQLAlchemyWorkScheduleRepository(session)
        )

        self.work_schedule_day_repository = (
            SQLAlchemyWorkScheduleDayRepository(session)
        )

        # -----------------------------------------------------------------
        # Leave repositories
        # -----------------------------------------------------------------

        self.leave_type_repository = SQLAlchemyLeaveTypeRepository(
            session,
        )

    def __enter__(self) -> "SQLAlchemyUnitOfWork":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if exc is None:
            self.commit()
        else:
            self.rollback()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()

    def flush(self) -> None:
        self._session.flush()