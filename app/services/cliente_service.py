from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas import ClientCreate, ClientResponse, ClientUpdate
from app.services.pipefy_service import (
    build_create_card_mutation,
    build_update_card_field_mutation,
)


async def create_client(
    db: AsyncSession, data: ClientCreate
) -> tuple[ClientResponse, dict]:
    cliente = await crud.create_client(db, data)
    mutation_payload = build_create_card_mutation(
        name=cliente.nome,
        email=cliente.email,
        valor_patrimonio=float(cliente.valor_patrimonio),
    )
    return ClientResponse.model_validate(cliente), mutation_payload


async def update_client(
    db: AsyncSession, data: ClientUpdate
) -> tuple[ClientResponse, dict]:
    event = await crud.get_webhook_event(db, data.event_id)
    if event is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Evento duplicado."
        )

    newEvent = await crud.create_webhook_event(db, data)
    cliente = await crud.get_cliente_by_email(db, newEvent.cliente_email)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cliente não encontrado."
        )

    if cliente.valor_patrimonio >= 200000:
        cliente = await crud.update_cliente_priority(db, cliente, "prioridade_alta")
    else:
        cliente = await crud.update_cliente_priority(db, cliente, "prioridade_normal")
    mutation_payload = build_update_card_field_mutation(
        card_id=newEvent.card_id, priority=cliente.prioridade
    )
    return ClientResponse.model_validate(cliente), mutation_payload
