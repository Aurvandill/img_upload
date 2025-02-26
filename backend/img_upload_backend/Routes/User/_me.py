import i18n
import bcrypt
import datetime

from uuid import uuid4
from sanic import Request
from typing import Optional
from sanic.exceptions import BadRequest
from sanic.response import json as json_resp
from sanic_ext import openapi

from img_upload_backend.Utility import ImageHandler
from img_upload_backend.data_models import User, IdentityToken, Image
from img_upload_backend.Utility.Decorators import (
    request_contains_valid_json,
    get_id_token,
)
from . import user_bp


@user_bp.route("/me", ["GET"], name="show_me")
@openapi.response(
    200,
    description="A JSON object containing information about the current user",
    content={
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "format": "uuid",
                        "description": "The uuid of the user",
                        "example": "2923ef3d-47cc-4d1f-a519-ff2cf669e3b2",
                    },
                    "username": {
                        "type": "string",
                        "description": "The username of the user",
                        "example": "example_user",
                    },
                    "admin": {"type": "boolean", "example": False},
                    "member_since": {
                        "type": "string",
                        "description": "When the user joined",
                        "example": "2025-07-13",
                    },
                    "created_at": {
                        "type": "string",
                        "description": "When the user was created",
                        "example": "2021-07-27T16:02:08.070Z",
                    },
                    "modified_at": {
                        "type": "string",
                        "description": "When the user was last modified",
                        "example": "2021-07-27T16:02:08.070Z",
                    },
                },
            },
        },
    },
)
@get_id_token
async def me(request: Request):
    """show me

    Show currently logged in user


    """

    id_token: IdentityToken = request.ctx.id_token

    user: User = await id_token.user

    resp_data = await user.serialize(True)

    return json_resp(resp_data)


@user_bp.route("/me", ["PATCH"], name="update_me")
@request_contains_valid_json
@get_id_token
async def update_me(request: Request):
    id_token: IdentityToken = request.ctx.id_token
    user: User = await id_token.user
    request_data = request.json

    birthday = request_data.get("birthday", None)
    email = request_data.get("email", None)
    new_password = request_data.get("password", None)
    old_password = request_data.get("old_password", None)

    # return a success message
    resp = json_resp(
        {
            "msg": i18n.t("messages.update_successfull"),
            "msg_key": "messages.update_successfull",
        }
    )

    if (
        birthday is None
        and email is None
        and new_password is None
        and old_password is None
    ):
        raise BadRequest(
            {
                "msg": i18n.t("errors.no_data_to_update"),
                "msg_key": "errors.no_data_to_update",
            }
        )

    if birthday is not None:
        user.birthday = datetime.date.fromisoformat(birthday)

    if email is not None:
        user.email = email

    if new_password is not None and old_password is not None:
        if not bcrypt.checkpw(old_password.encode("utf-8"), user.password_hash):
            raise BadRequest(
                {
                    "msg": i18n.t("errors.update_wrong_password"),
                    "msg_key": "errors.update_wrong_password",
                },
            )

        salt = bcrypt.gensalt()
        pw_hash = bcrypt.hashpw(new_password.encode("utf-8"), salt)
        user.password_hash = pw_hash

    await user.save()

    # get all identity tokens and delete them
    tokens_to_delete = await user.identity_tokens.all()

    # delete them
    for token in tokens_to_delete:
        await token.delete()

    # tell the browser to delete the tokens as well
    resp.delete_cookie("IdentityToken")
    resp.delete_cookie("RefreshToken")

    return resp


@user_bp.route("/me", ["DELETE"], name="delete_me")
@get_id_token
async def delete_me(
    request: Request,
):
    id_token: IdentityToken = request.ctx.id_token
    user: User = await id_token.user

    user_avatar: Optional[Image] = await user.avatar
    if user_avatar is not None:
        image_handler: ImageHandler = request.app.ctx.image_handler
        await image_handler.remove_file(str(user_avatar.uuid))
        await user_avatar.delete()

    await user.delete()
    resp = json_resp(
        {"msg": i18n.t("messages.user_deleted"), "msg_key": "messages.user_deleted"}
    )
    # tell the browser to delete the tokens as well
    resp.delete_cookie("IdentityToken")
    resp.delete_cookie("RefreshToken")
    return resp
