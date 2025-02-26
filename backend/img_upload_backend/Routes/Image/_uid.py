import i18n

from sanic import Request
from uuid import UUID
from typing import Optional

from img_upload_backend.data_models import Image, IdentityToken, User
from img_upload_backend.Utility import ImageHandler
from img_upload_backend.Exceptions import ImageDoesNotExist
from img_upload_backend.Utility.Decorators import get_id_token

from . import image_bp


@image_bp.route("/<image_id:uuid>", ["GET"])

async def get_image(request: Request, image_id: UUID):
    image = await Image.get_or_none(uuid=image_id)
    if image is None:
        raise ImageDoesNotExist(
            {
                "msg": i18n.t("errors.image_does_not_exist"),
                "msg_key": "errors.image_does_not_exist",
            },
            status_code=404,
        )

    image_handler: ImageHandler = request.app.ctx.image_handler

    return await image_handler.get_file(image_id, image.filename)


from . import image_bp

@image_bp.route("/<image_id:uuid>", ["DELETE"], name="delete_img")
@get_id_token
async def del_image(request: Request, image_id: UUID):
    image:Optional[Image] = await Image.get_or_none(uuid=image_id)
    if image is None:
        raise ImageDoesNotExist(
            {
                "msg": i18n.t("errors.image_does_not_exist"),
                "msg_key": "errors.image_does_not_exist",
            },
            status_code=404,
        )

    image_handler: ImageHandler = request.app.ctx.image_handler

    id_token: IdentityToken = request.ctx.id_token
    user:User = await id_token.user
    img_uploader = await image.uploaded_by
    if user != img_uploader and not user.admin:
        # raise permission error
        raise ImageDoesNotExist(
            {
                "msg": i18n.t("errors.image_does_not_exist"),
                "msg_key": "errors.image_does_not_exist",
            },
            status_code=404,
        )
    
    await image_handler.remove_file(str(image_id))
    await image.delete()


from . import image_bp


@image_bp.route("/<image_id:uuid>/thumbnail", ["GET"])
async def get_image_thumbnail(request: Request, image_id: UUID):
    image = await Image.get_or_none(uuid=image_id)
    if image is None:
        raise ImageDoesNotExist()

    image_handler: ImageHandler = request.app.ctx.image_handler
    if image_handler.exists(f"{image_id}_thumbnail"):
        img_resp = await image_handler.get_file(
            f"{image_id}_thumbnail", f"{image.filename}_thumbnail.webp"
        )
    else:
        img_resp = await image_handler.get_file(image_id, image.filename)

    return img_resp
