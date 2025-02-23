import i18n
import bcrypt

from sanic import Request
from sanic.response import json as json_resp
from tortoise.exceptions import ValidationError

from img_upload_backend.data_models import User
from img_upload_backend.Utility import JWTHelper
from img_upload_backend.Utility.Decorators import request_contains_valid_json
from img_upload_backend.Exceptions import LoginError
from . import session_bp


@session_bp.route("/login", ["POST"])
@request_contains_valid_json
async def login(request: Request):
    request_data = request.json
    username = request_data.get("username", None)
    password = request_data.get("password", None)
    if username is None or username == "":
        raise LoginError(
            {
                "msg": i18n.t("errors.login_not_provided"),
                "msg_key": "errors.login_not_provided",
            },
            status_code=400,
        )
    if password is None:
        raise LoginError(
            {
                "msg": i18n.t("errors.password_not_providied"),
                "msg_key": "errors.password_not_providied",
            },
            status_code=400,
        )

    login_data = {"username": username}

    user = None
    try:
        user = await User.get_or_none(**login_data)
    except ValidationError:
        # this will get thrown if the username is to short
        raise LoginError(
            {
                "msg": i18n.t("errors.login_no_user"),
                "msg_key": "errors.login_no_user",
            },
            status_code=400,
        )
    if user is None:
        raise LoginError(
            {
                "msg": i18n.t("errors.login_no_user").format(username=username),
                "msg_key": "errors.login_no_user",
            },
            status_code=400,
        )

    if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
        raise LoginError(
            {
                "msg": i18n.t("errors.login_wrong_password").format(username=username),
                "msg_key": "errors.login_wrong_password",
            },
            status_code=400,
        )

    jwt_helper: JWTHelper = request.app.ctx.jwt
    identity, id_token = await jwt_helper._id_token(user)
    refresh_token = await jwt_helper._refresh_token(identity)

    resp = json_resp(
        {
            "msg": i18n.t("messages.login_success").format(username=username),
            "msg_key": "messages.login_success",
        }
    )

    resp.cookies.add_cookie(
        "IdentityToken",
        id_token,
        httponly=True,
        max_age=jwt_helper.valid_minutes_id * 60,
        secure=not request.app.debug,
    )
    resp.cookies.add_cookie(
        "RefreshToken",
        refresh_token,
        httponly=True,
        max_age=jwt_helper.valid_minutes_refresh * 60,
        secure=not request.app.debug,
    )

    return resp
