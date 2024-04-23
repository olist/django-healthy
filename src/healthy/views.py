# SPDX-FileCopyrightText: 2024-present OLIST TINY TECNOLOGIA LTDA
#
# SPDX-License-Identifier: MIT
from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
async def ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Pong", status=HTTPStatus.OK)
