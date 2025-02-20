import i18n
import bcrypt

from datetime import date
from tortoise.exceptions import ValidationError
from sanic import Request
from sanic.response import json as json_resp

from img_upload_backend.data_models import User
from img_upload_backend.Exceptions import RegistrationFail
from img_upload_backend.Utility.Decorators import request_contains_valid_json
from . import user_bp


@request_contains_valid_json
@user_bp.route("/register", ["POST"])
async def register(request: Request):

    request_body = request.json

    username = request_body.get("username", None)
    password = request_body.get("password", None)
    birthday = request_body.get("birthday", None)
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

    if username is None or password is None:
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.missing_parameters"),
                "msg_key": "errors.missing_parameters",
            },
            status_code=400,
        )
    # see if the user provided a birthday and if so convert it to a date object
    try:
        if birthday is not None:
            birthday = date.fromisoformat(birthday)
    except ValueError:
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.birthday_invalid"),
                "msg_key": "errors.birthday_invalid",
            },
            status_code=400,
        )
    # see if the user provided email is not taken
    try:
        if await User.get_or_none(username=username) is not None:
            raise RegistrationFail(
                {
                    "msg": i18n.t("errors.username_taken").format(username=username),
                    "msg_key": "errors.username_taken",
                },
                status_code=400,
            )
    except ValidationError:
        # this will get thrown if the email does not match the email regex
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.username_invalid"),
                "msg_key": "errors.username_invalid",
            },
            status_code=400,
        )
    try:
        user = await User.create(username=username, password_hash=pw_hash)
        await user.save()
    except ValidationError:
        # this error should not be possible because we already checked the email and username for validity
        raise RegistrationFail(
            {
                "msg": i18n.t("errors.validation_error"),
                "msg_key": "errors.validation_error",
            },
            status_code=400,
        )

    return json_resp(
        {
            "msg": i18n.t("messages.user_created").format(
                username=request_body["username"]
            ),
            "msg_key": "messages.user_created",
        }
    )
