import i18n

from sanic import Blueprint, Request
from sanic.response import json as json_resp

user_bp = Blueprint("User", "/User")

from img_upload_backend.data_models import User
from img_upload_backend.Exceptions import ParameterError
from . import _register, _me, _uid


@user_bp.route("/", ["GET"])
async def show_users(request: Request):
    """Show Users

    This Functions returns all users.

    openapi:
    ---
    parameters:
    - name: pagesize
      in: query
      description: Numbers of users per page
      required: false
      default: 25
    - name: page
      in: query
      description: which page of all users to display
      required: false
      default: 1
    responses:
      '200':
        description: A JSON object containing the user count and user details
        content:
          application/json:
            schema:
              type: object
              properties:
                user_count:
                  type: integer
                  description: The total number of users
                  example: 100
                users:
                  type: object
                  additionalProperties:
                    type: string
                    format: uuid
                  description: A map of user UUIDs to usernames
                  example:
                    b77cc1a0-91ec-4d64-bb6d-21717737ea3c: test_user
                    19f401ba-e8b0-48c4-8c77-b0ebb26d97fe: another_user

    """
    request_args: dict = request.args
    try:
        page = int(request_args.get("page", 1))
    except ValueError:
        raise ParameterError(
            {
                "msg": i18n.t("errors.parameter_error").format(parameter="page"),
                "msg_key": "errors.parameter_error",
            },
            400,
        )
    try:
        pagesize = int(request_args.get("pagesize", 25))
    except ValueError:
        raise ParameterError(
            {
                "msg": i18n.t("errors.parameter_error").format(parameter="pagesize"),
                "msg_key": "errors.parameter_error",
            },
            400,
        )
    user_count = await User.all().count()
    users = (
        await User.all()
        .offset((page - 1) * pagesize)
        .limit(pagesize)
        .values_list("username", "uuid")
    )
    print(users)
    for user in users:
        username, uid = user
        print(username, str(uid))
    results = {str(uuid): username for username, uuid in users}

    return json_resp({"user_count": user_count, "users": results})
