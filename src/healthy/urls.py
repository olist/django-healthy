# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from django.urls import path

from .views import LivenessView

app_name = "healthy"

urlpatterns = [
    path("ping/", LivenessView.as_view(), name="ping"),
]
