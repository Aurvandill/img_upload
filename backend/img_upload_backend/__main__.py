import bcrypt
import tomllib
import logging

from sanic import Sanic
from pathlib import Path
from typing import Optional
from functools import partial
from sanic.worker.loader import AppLoader

from img_upload_backend.Enums import SignMethod
from img_upload_backend import create_app, cli
from img_upload_backend.data_models import User

logger = logging.getLogger("img_upload_backend")


async def define_users(_app, _loop, user_config: Optional[list[dict]] = None):
    if user_config is None:
        return
    for user_data in user_config:

        username = user_data["username"]
        password = user_data["password"]
        admin = user_data.get("admin", False)

        user = await User.get_or_none(username=username)
        if user is not None:
            logger.info(f"{username} already exists skipping creation")
            continue

        logger.info(f"creating user {username}")

        salt = bcrypt.gensalt()
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

        user = await User.create(username=username, password_hash=pw_hash, admin=admin)
        await user.save()


if __name__ == "__main__":
    config_file = cli()
    cfg = tomllib.loads(Path(config_file).read_text())
    cfg["JWT"]["signmethod"] = SignMethod(cfg["JWT"].pop("algorithm"))

    loader = AppLoader(factory=partial(create_app, cfg))
    app = loader.load()

    app.prepare(
        host=cfg.get("listening_ip", "localhost"),
        port=cfg.get("port", 9999),
        dev=cfg.get("debug", False),
    )
    print("reeeeeeeeee")
    print(cfg["users"])
    app.register_listener(
        partial(define_users, user_config=cfg.get("users", None)), "main_process_start"
    )

    Sanic.serve(primary=app, app_loader=loader)
