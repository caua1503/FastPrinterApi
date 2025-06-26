from enum import Enum

from pydantic import BaseModel


class WebhookTypeSchema(str, Enum):
    error = "error"
    alert_clean = "alert_clean"


class WebhookBaseSchema(BaseModel):
    message: str
    type: WebhookTypeSchema
    date: str


class WebhookDefaultSchema(WebhookBaseSchema): ...
