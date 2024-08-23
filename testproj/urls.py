# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from django.urls import include, path

urlpatterns = [
    path("", include("healthy.urls", namespace="healthy")),
]
