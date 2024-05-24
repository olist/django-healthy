# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from unittest import mock

import pytest
from django.core.files.storage import storages
from django.db import connections
from healthy import backends
from healthy.compat import override


class TestHealth:
    def test_up_without_args(self):
        got = backends.Health.up()

        assert got.status == backends.HealthStatus.UP
        assert got.details == {}

    def test_up_with_mapping_details(self):
        given_details = {"message": "It's fine!"}
        got = backends.Health.up(given_details)

        assert got.status == backends.HealthStatus.UP
        assert got.details == given_details

    def test_down_without_args(self):
        got = backends.Health.down()

        assert got.status == backends.HealthStatus.DOWN
        assert got.details == {}

    def test_down_with_mapping_details(self):
        given_details = {"message": "Something went wrong"}
        got = backends.Health.down(given_details)

        assert got.status == backends.HealthStatus.DOWN
        assert got.details == given_details

    def test_down_with_exception_details(self):
        given_message = "Something went wrong"
        got = backends.Health.down(RuntimeError(given_message))

        assert got.status == backends.HealthStatus.DOWN
        assert got.details == {"error": given_message}


@pytest.mark.asyncio
class TestHealthBackend:
    async def test_run_handles_exceptions(self):
        class FaultHealthBackend(backends.HealthBackend):
            @override
            async def run_health_check(self) -> backends.Health:
                msg = "Something went wrong"
                raise RuntimeError(msg)

        backend = FaultHealthBackend()
        got = await backend.run()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.DOWN
        assert "error" in got.details
        assert got.details["error"] == "Something went wrong"

    async def test_run_with_successful_check(self):
        expected = backends.Health.up({"message": "It's fine"})

        class ProxyHealthBackend(backends.HealthBackend):
            def __init__(self, health: backends.Health):
                self.health = health
                super().__init__()

            @override
            async def run_health_check(self) -> backends.Health:
                return self.health

        backend = ProxyHealthBackend(expected)
        got = await backend.run()

        assert got == expected


@pytest.mark.asyncio
class TestLivenessHealthBackend:
    async def test_run_health_check(self):
        backend = backends.LivenessHealthBackend()

        got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.UP


@pytest.mark.asyncio
class TestCacheHealthCheck:
    async def test_with_working_cache(self):
        backend = backends.CacheHealthBackend()

        got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.UP

    async def test_with_broken_cache(self):
        backend = backends.CacheHealthBackend("broken")

        got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.DOWN

    async def test_with_invalid_value(self):
        backend = backends.CacheHealthBackend("dummy")

        got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.DOWN


@pytest.mark.asyncio
class TestDatabasePingBackend:
    async def test_with_working_database(self):
        backend = backends.DatabasePingBackend()

        got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.UP

    async def test_with_unreachable_database(self):
        backend = backends.DatabasePingBackend()
        connection = connections[backend.alias]

        with mock.patch.object(connection, "is_usable", return_value=False):
            got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.DOWN

    async def test_with_database_error(self):
        backend = backends.DatabasePingBackend()
        connection = connections[backend.alias]

        with mock.patch.object(connection, "is_usable", side_effect=RuntimeError):
            got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.DOWN


@pytest.mark.asyncio
class TestStorageBackend:
    async def test_with_working_storage(self):
        backend = backends.StorageBackend()

        got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.UP

    async def test_with_save_error(self):
        backend = backends.StorageBackend()
        storage = storages[backend.alias]

        with mock.patch.object(storage, "save", side_effect=Exception):
            got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.DOWN

    async def test_with_noop_save(self):
        backend = backends.StorageBackend()
        storage = storages[backend.alias]

        with mock.patch.object(storage, "save"):
            got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.DOWN

    async def test_with_delete_error(self):
        backend = backends.StorageBackend()
        storage = storages[backend.alias]

        with mock.patch.object(storage, "delete", side_effect=Exception):
            got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.DOWN

    async def test_with_noop_delete(self):
        backend = backends.StorageBackend()
        storage = storages[backend.alias]

        with mock.patch.object(storage, "delete"):
            got = await backend.run_health_check()

        assert isinstance(got, backends.Health)
        assert got.status == backends.HealthStatus.DOWN
