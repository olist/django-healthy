# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from django.urls import path

from .views import PingView

app_name = "healthy"

urlpatterns = [
    path("ping/", PingView.as_view(), name="ping"),
]
