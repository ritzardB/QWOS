from __future__ import annotations

from pydantic import Field

from qwos.api.contracts.requests.common.base_request import BaseRequest


class PaginationRequest(BaseRequest):
    page: int = Field(default=1, ge=1)

    page_size: int = Field(default=25, ge=1, le=100)
