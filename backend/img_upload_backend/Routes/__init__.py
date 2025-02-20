from sanic import Blueprint
from sanic.response import json as json_resp

from .User import user_bp
from .Session import session_bp
from .Image import image_bp
from img_upload_backend.Utility.Middleware import add_token_info

generic_bp = Blueprint.group(user_bp, session_bp, image_bp, url_prefix="/")

for bp in generic_bp:
    bp.middleware(add_token_info, "request")

#user_bp middleware(add_token_info, "request")
#session_bp.middleware(add_token_info, "request")
#image_bp.middleware(add_token_info, "request")
