# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
import json
from http import HTTPStatus

from healthy.backends import Health
from healthy.responses import HealthResponse


class TestHealthResponse:
    def test_with_up_health(self):
        health = Health.up({"message": "It's fine"})
        response = HealthResponse(health)

        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.content) == {"status": "up", "details": {"message": "It's fine"}}

    def test_with_down_health(self):
        health = Health.down({"message": "Something went wrong"})
        response = HealthResponse(health)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert json.loads(response.content) == {"status": "down", "details": {"message": "Something went wrong"}}
