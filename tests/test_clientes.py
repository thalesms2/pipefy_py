from app.crud import get_cliente_by_email


async def test_criar_cliente_com_payload_valido(client):
    payload = {
        "cliente_nome": "João Silva",
        "cliente_email": "joao@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 150000,
    }
    response = await client.post("/clientes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "João Silva"
    assert data["email"] == "joao@example.com"
    assert data["tipo_solicitacao"] == "Atualização cadastral"
    assert float(data["valor_patrimonio"]) == 150000.0
    assert data["prioridade"] is None


async def test_criar_cliente_salva_no_banco(client, db_session):
    payload = {
        "cliente_nome": "Maria Oliveira",
        "cliente_email": "maria@example.com",
        "tipo_solicitacao": "Novo investimento",
        "valor_patrimonio": 50000,
    }
    response = await client.post("/clientes", json=payload)
    assert response.status_code == 201

    cliente = await get_cliente_by_email(db_session, "maria@example.com")
    assert cliente is not None
    assert cliente.nome == "Maria Oliveira"
    assert cliente.tipo_solicitacao == "Novo investimento"
    assert float(cliente.valor_patrimonio) == 50000.0
