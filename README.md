# Mundo Invest - Client Management & Pipefy Integration

Este repositório contém a minha solução para o desafio técnico de Backend do Mundo Invest. O objetivo do serviço é gerenciar a entrada de clientes e seus patrimônios, além de simular a persistência local e o mapeamento de mutations GraphQL que interagiriam com o Pipefy.

A aplicação foi desenhada focando em simplicidade, mas com uma arquitetura baseada em Clean Code e separação clara de responsabilidades (isolando domínio, aplicação e infraestrutura). Isso facilita muito a manutenção e garante uma base sólida para a implementação dos testes.

## Tecnologias Utilizadas
* **Linguagem:** Python 3.11+.
* **Banco de Dados:** PostgreSQL (via Docker). 
* **Testes:** `pytest` para garantir a cobertura das regras de negócio (foco em TDD).
* **Integração:** Estruturação rigorosa das mutations GraphQL baseadas na documentação do Pipefy (`createCard` e `updateCardField`).

## Como rodar o projeto localmente

### Pré-requisitos
* Python 3.11 ou superior
* Docker e Docker Compose 

### Passo a Passo
1. Clone este repositório:
```bash
   git clone https://github.com/thalesms2/pipefy_py.git
   cd pipefy_py 
```
2. Copie o arquivo `.env.example` e renomeie para `.env`.

3. Execute a aplicação e o banco de dados:
```bash
docker-compose up 
```
 
A API estará rodando na porta 8000 (ou a porta configurada no seu app).

## Rodando os Testes Automatizados
Fiz questão de cobrir os fluxos principais com testes automatizados, validando a criação de clientes, a regra de negócio dos patrimônios e, de forma crucial, o bloqueio de processamento duplicado (idempotência) pelo event_id.

Para rodar a suíte de testes:

```bash
pytest tests/test_clientes.py -v
pytest tests/test_webhook.py -v
```

## Exemplos de Requisição (cURL)
1. Criação de Cliente e Mapeamento de Card
Endpoint: POST /clientes

Neste fluxo, o cliente é salvo com o status "Aguardando Análise" e o payload GraphQL (createCard) é montado na camada de serviço.

```bash
curl --location 'localhost:8000/clientes' \
--header 'Content-Type: application/json' \
--data-raw '{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000
}'
```

2. Atualização de Card via Webhook
Endpoint: POST /webhooks/pipefy/card-updated

Este endpoint simula o retorno do Pipefy. Ele garante a idempotência validando o event_id, aplica a regra de prioridade baseada no patrimônio e monta a mutation (updateCardField).

```bash
curl --location 'localhost:8000/webhook/pipefy/card-updated' \
--header 'Content-Type: application/json' \
--data-raw '{
  "event_id": "evt_43211",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}'
```
