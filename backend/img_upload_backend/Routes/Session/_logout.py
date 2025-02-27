import i18n

from datetime import datetime
from tortoise import timezone
from sanic import Request, BadRequest
from sanic.response import json as json_resp

from img_upload_backend.Exceptions import SessionError
from img_upload_backend.data_models import IdentityToken, User
from img_upload_backend.Utility.Decorators import get_id_token
from . import session_bp


@session_bp.route("/logout", ["POST"], name="logout")
@get_id_token
async def logout(request: Request):
    id_token: IdentityToken = request.ctx.id_token
    request_data = None
    try:
        request_data = request.json
    except BadRequest:
        # if the request has no valid json ignore it
        pass
    if request_data is None:
        # if no json was provided we use an empty dict
        request_data = {}

    if id_token.valid_until < timezone.now():
        raise SessionError(
            {
                "msg": i18n.t("errors.session_expired"),
                "msg_key": "errors.session_expired",
            },
            status_code=400,
        )

    tokens_to_delete: list[IdentityToken] = []

    if request_data.get("logout_all", False):
        # the user wants to destroy all Sessions
        # so we need to get all IdentityTokens belonging to the user
        user: User = await id_token.user
        # add them to the list of tokens to delete
        tokens_to_delete = await user.identity_tokens.all()
    else:
        # if the user wants to log out jsut this session
        # only add the current token to the list of tokens to be deleted
        tokens_to_delete.append(id_token)

    # finaly delete the tokens
    for token in tokens_to_delete:
        await token.delete()

    # return a success message
    resp = json_resp(
        {
            "msg": i18n.t("messages.logout_success"),
            "msg_key": "messages.logout_success",
        }
    )

    # tell the browser to delete the tokens as well
    resp.delete_cookie("IdentityToken")
    resp.delete_cookie("RefreshToken")

    return resp
