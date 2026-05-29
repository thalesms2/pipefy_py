from app.crud import get_cliente_by_email


async def _criar_cliente(client, email: str, valor_patrimonio: float):
    await client.post("/clientes", json={
        "cliente_nome": "João Silva",
        "cliente_email": email,
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": valor_patrimonio,
    })


async def test_webhook_impede_event_id_duplicado(client):
    await _criar_cliente(client, "joao@example.com", 250000)
    payload = {
        "event_id": "evt-001",
        "card_id": "card-001",
        "cliente_email": "joao@example.com",
        "timestamp": "2024-01-01T10:00:00",
    }
    await client.post("/webhook/pipefy/card-updated", json=payload)
    response = await client.post("/webhook/pipefy/card-updated", json=payload)
    assert response.status_code == 409


async def test_webhook_define_prioridade_alta_para_patrimonio_igual_ou_acima_200000(
    client, db_session
):
    await _criar_cliente(client, "joao@example.com", 200000)
    payload = {
        "event_id": "evt-002",
        "card_id": "card-002",
        "cliente_email": "joao@example.com",
        "timestamp": "2024-01-01T10:00:00",
    }
    response = await client.post("/webhook/pipefy/card-updated", json=payload)
    assert response.status_code == 200

    cliente = await get_cliente_by_email(db_session, "joao@example.com")
    assert cliente.prioridade == "prioridade_alta"
