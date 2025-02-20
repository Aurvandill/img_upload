import datetime

from uuid import UUID
from tortoise import fields
from tortoise.models import Model


class Image(Model):
    uuid: UUID = fields.UUIDField(primary_key=True)
    filename = fields.TextField()
    created_at: datetime.datetime = fields.DatetimeField(
        auto_now_add=True,
        allows_generated=True,
        GENERATED_SQL="NOW()",
        description="When was this image added to the Database",
    )
    uploaded_by = fields.ForeignKeyField(
        model_name="data_models.User",
        null=True,
        on_delete=fields.OnDelete.SET_NULL,
        related_name="images",
    )
