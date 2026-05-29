from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Cliente, WebhookEvent
from app.schemas import ClientCreate, ClientUpdate


async def create_client(db: AsyncSession, data: ClientCreate) -> Cliente:
    cliente = Cliente(
        nome=data.cliente_nome,
        email=data.cliente_email,
        tipo_solicitacao=data.tipo_solicitacao,
        valor_patrimonio=Decimal(str(data.valor_patrimonio)),
    )
    db.add(cliente)
    await db.commit()
    await db.refresh(cliente)
    return cliente


async def get_cliente_by_email(db: AsyncSession, email: str) -> Cliente | None:
    result = await db.execute(select(Cliente).where(Cliente.email == email))
    return result.scalar_one_or_none()


async def update_cliente_priority(
    db: AsyncSession, cliente: Cliente, priority: str
) -> Cliente:
    cliente.prioridade = priority
    await db.commit()
    await db.refresh(cliente)
    return cliente


async def get_webhook_event(db: AsyncSession, event_id: str) -> WebhookEvent | None:
    result = await db.execute(
        select(WebhookEvent).where(WebhookEvent.event_id == event_id)
    )
    return result.scalar_one_or_none()


async def create_webhook_event(db: AsyncSession, data: ClientUpdate) -> WebhookEvent:
    event = WebhookEvent(
        event_id=data.event_id,
        card_id=data.card_id,
        cliente_email=data.cliente_email,
        processed_at=data.timestamp,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event
