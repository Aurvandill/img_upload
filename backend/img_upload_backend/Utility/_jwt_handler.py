import jwt
import datetime

from uuid import UUID
from typing import Optional
from dataclasses import dataclass
from jwt.exceptions import InvalidTokenError

from img_upload_backend.Enums import SignMethod
from img_upload_backend.data_models import IdentityToken, RefreshToken, User


@dataclass
class JWTHelper:
    issuer: str
    signmethod: SignMethod
    secret: str
    valid_minutes_id: int = 60
    valid_minutes_refresh: int = 1440

    async def _id_token(self, user: User, id_token: Optional[IdentityToken] = None):
        valid_until = datetime.datetime.now() + datetime.timedelta(
            minutes=self.valid_minutes_id
        )

        if id_token is None:

            id_token = await IdentityToken.create(user=user, valid_until=valid_until)

        jwt_header = {"kid": str(id_token.uuid), "token": "IdentityToken"}

        jwt_data = {
            "iss": self.issuer,
            "iat": datetime.datetime.now().timestamp(),
            "nbf": datetime.datetime.now().timestamp(),
            "exp": valid_until.timestamp(),
            "user": await user.serialize(),
        }

        token = jwt.encode(
            jwt_data,
            self.secret,
            headers=jwt_header,
            algorithm=self.signmethod.value,
        )

        return id_token, token

    async def _refresh_token(
        self, id_token: IdentityToken, refresh_token: Optional[RefreshToken] = None
    ):
        valid_until = datetime.datetime.now() + datetime.timedelta(
            minutes=self.valid_minutes_refresh
        )
        if refresh_token is None:

            refresh_token = await RefreshToken.create(
                valid_until=valid_until, id_token=id_token
            )

        jwt_header = {"kid": str(refresh_token.uuid), "token": "RefreshToken"}

        jwt_data = {
            "iss": self.issuer,
            "iat": datetime.datetime.now().timestamp(),
            "nbf": datetime.datetime.now().timestamp(),
            "exp": valid_until.timestamp(),
            "id_token": str(id_token.uuid),
        }

        token = jwt.encode(
            jwt_data,
            self.secret,
            headers=jwt_header,
            algorithm=self.signmethod.value,
        )

        return token

    def token_data(self, id_token: str) -> tuple[dict[str, str], UUID]:
        jwt_data = jwt.decode(id_token, self.secret, self.signmethod.value)
        user_data = jwt_data.get("user", None)
        if user_data is None:
            raise InvalidTokenError()

        id_token_id = jwt.get_unverified_header(id_token).get("kid", None)

        if id_token_id is None:
            raise InvalidTokenError()

        try:
            id_token_id = UUID(id_token_id)
        except ValueError:
            raise InvalidTokenError()

        return user_data, id_token_id

    def token_lifetime(self, token: str) -> Optional[bool]:
        token_lifetime = jwt.decode(
            token, self.secret, self.signmethod.value, verify=False
        ).get("exp", None)
        return token_lifetime

    async def renew_tokens(self, refresh_token: str) -> tuple[ſtr, str]:
        # validate jwt
        jwt_data = jwt.decode(refresh_token, self.secret, self.signmethod.value)

        id_token_id = jwt_data.get("id_token", None)
        # check if the token has a id_token id given
        if id_token_id is None:
            raise InvalidTokenError()

        # check if the header has a refresh token id given
        refresh_token_id = jwt.get_unverified_header(refresh_token).get("kid", None)
        if refresh_token_id is None:
            raise InvalidTokenError()

        # try to get refresh_token via id
        try:
            refresh_token_obj = await RefreshToken.get_or_none(
                uuid=UUID(refresh_token_id)
            )
        except ValueError:
            # if the UUID is invalid
            raise InvalidTokenError()

        if refresh_token_obj is None:
            raise InvalidTokenError()

        # try to get id_token via id
        try:
            id_token = await IdentityToken.get_or_none(uuid=UUID(id_token_id))
        except ValueError:
            # if the UUID is invalid
            raise InvalidTokenError()

        if id_token is None:
            # no id token with given id... not gonna create a new one
            raise InvalidTokenError()

        valid_until = datetime.datetime.now() + datetime.timedelta(
            minutes=self.valid_minutes_id
        )

        id_token.valid_until = valid_until
        await id_token.save()

        jwt_header = {"kid": str(id_token.uuid), "token": "IdentityToken"}
        jwt_data = {
            "iss": self.issuer,
            "iat": datetime.datetime.now().timestamp(),
            "nbf": datetime.datetime.now().timestamp(),
            "exp": valid_until.timestamp(),
            "id_token": str(id_token.uuid),
        }

        updated_id_token = jwt.encode(
            jwt_data,
            self.secret,
            headers=jwt_header,
            algorithm=self.signmethod.value,
        )

        _, updated_id_token = await self._id_token(await id_token.user, id_token)

        valid_until = datetime.datetime.now() + datetime.timedelta(
            minutes=self.valid_minutes_refresh
        )
        refresh_token_obj.valid_until = valid_until
        await refresh_token_obj.save()

        jwt_header = {"kid": str(refresh_token_obj.uuid), "token": "RefreshToken"}

        jwt_data = {
            "iss": self.issuer,
            "iat": datetime.datetime.now().timestamp(),
            "nbf": datetime.datetime.now().timestamp(),
            "exp": valid_until.timestamp(),
            "id_token": str(id_token.uuid),
        }

        updated_refresh_token = jwt.encode(
            jwt_data,
            self.secret,
            headers=jwt_header,
            algorithm=self.signmethod.value,
        )

        return updated_id_token, updated_refresh_token
