# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
import asyncio
from dataclasses import asdict
from typing import ClassVar

from django.http import HttpRequest, HttpResponse
from django.views import View

from .backends import Health, HealthStatus, LivenessHealthBackend
from .handler import health_checks
from .responses import HealthResponse


class LivenessView(View):
    http_method_names: ClassVar = [
        "get",
        "head",
        "options",
        "trace",
    ]

    async def get(self, request: HttpRequest) -> HttpResponse:  # noqa: ARG002
        backend = LivenessHealthBackend()
        health = await backend.run()
        return HealthResponse(health)


class HealthView(View):
    http_method_names: ClassVar = [
        "get",
        "head",
        "options",
        "trace",
    ]

    async def get(self, request: HttpRequest) -> HttpResponse:  # noqa: ARG002
        tasks = [health_checks[alias].run() for alias in health_checks]
        indicators = await asyncio.gather(*tasks)
        details = {alias: asdict(indicator) for alias, indicator in zip(health_checks, indicators)}

        if any(health.status == HealthStatus.DOWN for health in indicators):
            health = Health.down(details)
        else:
            health = Health.up(details)

        return HealthResponse(health)
