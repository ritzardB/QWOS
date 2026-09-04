from typing import Protocol

from qwos.domains.leave.models.leave_policy import LeavePolicy


class LeavePolicyRepository(Protocol):
    def get_by_id(self, leave_policy_id: str) -> LeavePolicy | None: ...

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: str,
        leave_policy_id: str,
    ) -> LeavePolicy | None: ...

    def save(self, leave_policy: LeavePolicy) -> None: ...

    def list_by_tenant(
        self,
        *,
        tenant_id: str,
    ) -> list[LeavePolicy]: ...

    def get_active_by_code(
        self,
        *,
        tenant_id: str,
        policy_code: str,
    ) -> LeavePolicy | None: ...

    def exists_by_code(
        self,
        *,
        tenant_id: str,
        policy_code: str,
    ) -> bool: ...