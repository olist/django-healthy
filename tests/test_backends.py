# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
import pytest
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
