from __future__ import annotations

from qwos.api.contracts.requests.common.base_request import BaseRequest


class SortingRequest(BaseRequest):
    sort_by: str | None = None

    descending: bool = False
