# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
import json
from http import HTTPStatus

from healthy.backends import Health
from healthy.responses import HealthResponse


class TestHealthResponse:
    def test_with_healthy_health(self):
        health = Health.healthy({"message": "It's fine"})
        response = HealthResponse(health)

        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.content) == {"status": "healthy", "details": {"message": "It's fine"}}

    def test_with_unhealthy_health(self):
        health = Health.unhealthy({"message": "Something went wrong"})
        response = HealthResponse(health)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert json.loads(response.content) == {"status": "unhealthy", "details": {"message": "Something went wrong"}}
