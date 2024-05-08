# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from django.conf import settings
from django.utils.module_loading import import_string

from .backends import HealthBackend


class HealthHandler:
    def __init__(self):
        self.backends = settings.HEALTH_CHECK_BACKENDS
        self._checks = {}

    def __getitem__(self, alias: str) -> HealthBackend:
        if alias not in self._checks:
            params = self.backends[alias]
            check = self.create(params)
            self._checks[alias] = check
        return self._checks[alias]

    def __iter__(self):
        return iter(self.backends)

    def create(self, params: dict) -> HealthBackend:
        backend = params["BACKEND"]
        options = params.get("OPTIONS", {})

        backend_class = import_string(backend)
        return backend_class(**options)


health_checks = HealthHandler()
