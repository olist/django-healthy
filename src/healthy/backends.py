# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from io import StringIO
from time import perf_counter_ns
from typing import Final, overload

from asgiref.sync import sync_to_async
from django.core.cache import caches
from django.core.files.storage import Storage, storages
from django.db import connections

from .compat import Self, StrEnum, override


class HealthStatus(StrEnum):
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    HEALTHY = "healthy"


@dataclass
class Health:
    status: HealthStatus
    details: dict = field(default_factory=dict)

    @overload
    @classmethod
    def healthy(cls) -> Self: ...

    @overload
    @classmethod
    def healthy(cls, details: dict) -> Self: ...

    @classmethod
    def healthy(cls, details: dict | None = None) -> Self:
        if details is None:
            details = {}

        return cls(status=HealthStatus.HEALTHY, details=details)

    @overload
    @classmethod
    def unhealthy(cls) -> Self: ...

    @overload
    @classmethod
    def unhealthy(cls, details: Exception) -> Self: ...

    @overload
    @classmethod
    def unhealthy(cls, details: dict) -> Self: ...

    @classmethod
    def unhealthy(cls, details: dict | Exception | None = None) -> Self:
        if details is None:
            details = {}
        elif isinstance(details, Exception):
            details = {"error": str(details)}

        return cls(status=HealthStatus.UNHEALTHY, details=details)


class HealthBackend(ABC):
    async def run(self) -> Health:
        start_time_ns = perf_counter_ns()
        try:
            health = await self.run_health_check()
        except Exception as exc:  # noqa: BLE001
            health = Health.unhealthy(exc)

        end_time_ns = perf_counter_ns()
        health.details["time_ns"] = end_time_ns - start_time_ns

        return health

    @abstractmethod
    async def run_health_check(self) -> Health:
        """Run the health checking logic"""


class LivenessHealthBackend(HealthBackend):
    @override
    async def run_health_check(self) -> Health:
        return Health.healthy()


CACHE_VALUE: Final[str] = "healthy_test_value"


class CacheHealthBackend(HealthBackend):
    __slots__ = ("alias", "key")

    def __init__(self, alias: str = "default", key: str = "healthy_test"):
        self.alias = alias
        self.key = key

    async def run_health_check(self) -> Health:
        cache = caches[self.alias]
        given = CACHE_VALUE

        try:
            await cache.aset(self.key, given)
            got = await cache.aget(self.key)
            if got != given:
                return Health.unhealthy({"message": "Got unexpected value."})
        except Exception as exc:  # noqa: BLE001
            return Health.unhealthy(exc)

        return Health.healthy()


class DatabasePingBackend(HealthBackend):
    __slots__ = ("alias",)

    def __init__(self, alias: str = "default"):
        self.alias = alias

    async def run_health_check(self) -> Health:
        connection = connections[self.alias]
        try:
            await sync_to_async(connection.ensure_connection)()
            usable = await sync_to_async(connection.is_usable)()
            return Health.healthy() if usable else Health.unhealthy()
        except Exception as exc:  # noqa: BLE001
            return Health.unhealthy(exc)


class StorageBackend(HealthBackend):
    __slots__ = ("alias",)

    def __init__(self, alias: str = "default"):
        self.alias = alias

    async def run_health_check(self) -> Health:
        storage: Storage = storages[self.alias]
        content: str = "This is a django-healthy test file."

        try:
            filename = storage.get_alternative_name("healthy_test_file", ".txt")
            await sync_to_async(storage.save)(filename, StringIO(content))

            exists = await sync_to_async(storage.exists)(filename)
            if not exists:
                return Health.unhealthy({"reason": "Missing file"})

            await sync_to_async(storage.delete)(filename)
            exists = await sync_to_async(storage.exists)(filename)
            if exists:
                return Health.unhealthy({"reason": "Could not delete file"})
        except Exception as exc:  # noqa: BLE001
            return Health.unhealthy(exc)
        else:
            return Health.healthy()
