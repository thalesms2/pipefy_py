from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ClientResponse, ClientUpdate
from app.services.cliente_service import update_client

router = APIRouter(prefix="/webhook/pipefy/card-updated", tags=["webhook"])


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ClientResponse,
)
async def post_webhook(payload: ClientUpdate, db: AsyncSession = Depends(get_db)):
    client_response, mutation = await update_client(db, payload)
    print(mutation)
    return client_response
