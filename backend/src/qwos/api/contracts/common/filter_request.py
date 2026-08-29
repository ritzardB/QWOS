from __future__ import annotations

from qwos.api.contracts.requests.common.base_request import BaseRequest


class FilterRequest(BaseRequest):
    search: str | None = None

    is_active: bool | None = None
