# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from typing import ClassVar

from django.http import HttpRequest, HttpResponse
from django.views import View

from .backends import LivenessHealthBackend
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
