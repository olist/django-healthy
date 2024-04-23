# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from django.urls import path

from .views import ping

app_name = "healthy"

urlpatterns = [
    path("ping/", ping, name="ping"),
]
