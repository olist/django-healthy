# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from dataclasses import asdict
from http import HTTPStatus

from django.http import JsonResponse

from .backends import Health, HealthStatus


class HealthResponse(JsonResponse):
    def __init__(self, health: Health):
        status = HTTPStatus.OK if health.status == HealthStatus.UP else HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__(data=asdict(health), status=status)
