import i18n

from uuid import UUID
from sanic import Request
from sanic.response import json as json_resp

from img_upload_backend.data_models import User
from img_upload_backend.Exceptions import UserDoesNotExist

from . import user_bp


@user_bp.route("/<user_id:uuid>", ["GET"])
async def show_user_by_id(request: Request, user_id: UUID):
    user = await User.get_or_none(uuid=user_id)
    if user is None:
        raise UserDoesNotExist(
            {
                "msg": i18n.t("errors.user_does_not_exist").format(id=user_id),
                "msg_key": "errors.user_does_not_exist",
            },
            status_code=404,
        )

    repsonse_data = await user.serialize()

    # if the user is an admin we respond with the session token infos as well
    if request.ctx.user_info is not None and request.ctx.user_info.get("admin", False):
        repsonse_data["identity_tokens"] = await user.identity_tokens.all().values_list(
            "uuid", flat=True
        )

    return json_resp(repsonse_data)
