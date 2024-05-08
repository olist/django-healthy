# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from http import HTTPStatus

import pytest
from django.urls import reverse


class TestLivenessView:
    def test_get_ping(self, client):
        response = client.get(reverse("healthy:ping"))

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    def test_methods_not_allowed(self, method, client):
        django_client_method = getattr(client, method)

        response = django_client_method(reverse("healthy:ping"))

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    @pytest.mark.asyncio
    async def test_get_ping_async(self, async_client):
        response = await async_client.get(reverse("healthy:ping"))

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    async def test_methods_not_allowed_async(self, method, async_client):
        django_client_method = getattr(async_client, method)

        response = await django_client_method(reverse("healthy:ping"))

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


class TestHealthView:
    def test_get_health(self, client):
        response = client.get(reverse("healthy:health"))

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    def test_methods_not_allowed(self, method, client):
        django_client_method = getattr(client, method)

        response = django_client_method(reverse("healthy:health"))

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    @pytest.mark.asyncio
    async def test_get_health_async(self, async_client):
        response = await async_client.get(reverse("healthy:health"))

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    async def test_methods_not_allowed_async(self, method, async_client):
        django_client_method = getattr(async_client, method)

        response = await django_client_method(reverse("healthy:health"))

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
