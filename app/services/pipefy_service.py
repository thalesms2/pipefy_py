import os

PIPE_ID = os.getenv("PIPE_ID", "YOUR_PIPE_ID")

CREATE_CARD_MUTATION = """
mutation CreateNewCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
      title
    }
  }
}
"""

UPDATE_CARD_MUTATION = """
mutation UpdateCardPriority($inputPriority: UpdateCardFieldInput!, $inputStatus: UpdateCardFieldInput!) {
  priority: updateCardField(input: $inputPriority) {
    success
  }
  status: updateCardField(input: $inputStatus) {
    success
  }
}
"""


def build_create_card_mutation(name: str, email: str, valor_patrimonio: float) -> dict:
    return {
        "query": CREATE_CARD_MUTATION,
        "variables": {
            "input": {
                "pipe_id": PIPE_ID,
                "fields_attributes": [
                    {"field_id": "requester_name", "field_value": name},
                    {"field_id": "requester_email", "field_value": email},
                    {
                        "field_id": "requester_amount",
                        "field_value": str(valor_patrimonio),
                    },
                ],
            }
        },
    }


def build_update_card_field_mutation(card_id: str, priority: str) -> dict:
    return {
        "query": UPDATE_CARD_MUTATION,
        "variables": {
            "inputPriority": {
                "card_id": card_id,
                "field_id": "requester_priority",
                "new_value": priority,
            },
            "inputStatus": {
                "card_id": card_id,
                "field_id": "requester_status",
                "new_value": "Processado",
            },
        },
    }
