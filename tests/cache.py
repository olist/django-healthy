# ruff: noqa: ARG002
from __future__ import annotations

from typing import Any

from django.core.cache.backends.base import BaseCache


class BrokenCache(BaseCache):
    def __init__(self, host, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add(
        self,
        key: str,
        value: Any,
        timeout: int | None = None,
        version: int | None = None,
    ) -> bool:
        raise RuntimeError

    def get(
        self,
        key: str,
        default: Any | None = None,
        version: int | None = None,
    ) -> Any:
        raise RuntimeError

    def set(
        self,
        key: str,
        value: Any,
        timeout: int | None = None,
        version: int | None = None,
    ) -> None:
        raise RuntimeError

    def touch(
        self,
        key: str,
        timeout: int | None = None,
        version: int | None = None,
    ) -> bool:
        raise RuntimeError

    def delete(self, key: str, version: int | None = None) -> None:
        raise RuntimeError

    def clear(self) -> None:
        raise RuntimeError
