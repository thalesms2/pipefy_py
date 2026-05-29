# API Pipefy

## Instruções

Para rodar o projeto localmente copie o arquivo `.env.example` e renomeie para `.env` e execute o seguinte comando:
```bash
docker-compose up
```

Para rodar os testes, execute o projeto localmente e execute os seguintes comandos:
```bash
pytest tests/test_clientes.py -v
pytest tests/test_webhook.py -v
```

## Exemplo de requisições

```bash
# Criação do cliente e card no Pipefy
curl --location 'localhost:8000/clientes' \
--header 'Content-Type: application/json' \
--data-raw '{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000
}'
```

```bash
# Atualização via Webhook e definição de prioridade
curl --location 'localhost:8000/webhook/pipefy/card-updated' \
--header 'Content-Type: application/json' \
--data-raw '{
  "event_id": "evt_43211",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}'
```
