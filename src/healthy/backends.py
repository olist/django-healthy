# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import overload, Optional, Union

from .compat import Self, override, StrEnum

class HealthStatus(StrEnum):
    UP = "up"
    DOWN = "down"

@dataclass
class Health:
    status: HealthStatus
    details: dict = field(default_factory=dict)

    @overload
    @classmethod
    def up(cls) -> Self:
        ...

    @overload
    @classmethod
    def up(cls, details: dict) -> Self:
        ...

    @classmethod
    def up(cls, details: Optional[dict] = None) -> Self:
        if details is None:
            details = dict()

        return cls(status=HealthStatus.UP, details=details)

    @overload
    @classmethod
    def down(cls) -> Self:
        ...

    @overload
    @classmethod
    def down(cls, details: Exception) -> Self:
        ...

    @overload
    @classmethod
    def down(cls, details: dict) -> Self:
        ...

    @classmethod
    def down(cls, details: Optional[Union[dict, Exception]] = None) -> Self:
        if details is None:
            details = dict()
        elif isinstance(details, Exception):
            details = {"error": str(details)}

        return cls(status=HealthStatus.DOWN, details=details)


class HealthBackend(ABC):
    async def run(self) -> Health:
        try:
            health = await self.run_health_check()
        except Exception as exc:
            health = Health.down(exc)

        return health

    @abstractmethod
    async def run_health_check(self) -> Health:
        """Run the health checking logic"""


class LivenessHealthBackend(HealthBackend):
    @override
    async def run_health_check(self) -> Health:
        return Health.up()
