from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

from .page_metadata import PageMetadata

T = TypeVar("T")


class PagedResponse(BaseModel, Generic[T]):
    success: bool = True

    data: list[T]

    pagination: PageMetadata
