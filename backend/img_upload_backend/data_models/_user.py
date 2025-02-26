import re
import datetime

from uuid import UUID

from tortoise import fields
from tortoise.models import Model
from tortoise.validators import MinLengthValidator, RegexValidator


class User(Model):
    """Model Representing a User

    Attributes:
        username (str): Name of the User.
        password_hash (str, optional): Passwordhash for local Users
        auth_type (AuthSource): How to authenticate the User.
        email (str): Email address of the User.
        activated (bool): User verified his email Address.
    """

    uuid: UUID = fields.UUIDField(pk=True)
    username: str = fields.CharField(
        max_length=30,
        unique=True,
        description="Username",
        validators=[
            MinLengthValidator(5),
            RegexValidator(
                r"[a-z0-9]+[a-z \._-]+[a-z0-9]",
                re.I,
            ),
        ],
    )
    admin: bool = fields.BooleanField(default=False)
    password_hash: bytes = fields.BinaryField(
        description="Hash of the password", null=True
    )
    created_at: datetime.datetime = fields.DatetimeField(
        auto_now_add=True,
        allows_generated=True,
        GENERATED_SQL="NOW()",
        description="When was this User added to the Database",
    )
    modified_at: datetime.datetime = fields.DatetimeField(
        auto_now=True,
        allows_generated=True,
        GENERATED_SQL="NOW()",
        description="When was the user modified",
    )
    identity_tokens: fields.ReverseRelation["IdentityToken"]
    images: fields.ReverseRelation["Image"]

    @property
    def member_since(self):
        return self.created_at.strftime("%Y-%m-%d")

    async def serialize(self) -> dict:
        return {
            "id": str(self.uuid),
            "username": self.username,
            "admin": self.admin,
            "member_since": self.member_since,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
        }
