from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, field_validator


class ClientCreate(BaseModel):
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float

    @field_validator("cliente_nome", "tipo_solicitacao")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Campo não pode ser vazio")
        return v

    @field_validator("valor_patrimonio")
    @classmethod
    def patrimonio_positivo(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("valor_patrimonio deve ser positivo")
        return v


class ClientUpdate(BaseModel):
    event_id: str
    card_id: str
    cliente_email: EmailStr
    timestamp: datetime


class ClientResponse(BaseModel):
    id: int
    nome: str
    email: str
    tipo_solicitacao: str
    valor_patrimonio: Decimal
    prioridade: str | None

    model_config = {"from_attributes": True}


class WebhookPayload(BaseModel):
    event_id: str
    card_id: str
    cliente_email: EmailStr
    timestamp: datetime


class WebhookResponse(BaseModel):
    status: str
    message: str


class WebhookEvent(BaseModel):
    id: int
    event_id: str
    card_id: str
    cliente_email: str
    processed_at: datetime
