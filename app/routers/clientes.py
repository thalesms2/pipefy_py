from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ClientCreate, ClientResponse
from app.services.cliente_service import create_client

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ClientResponse)
async def post_client(payload: ClientCreate, db: AsyncSession = Depends(get_db)):
    client_response, mutation = await create_client(db, payload)
    print(mutation)
    return client_response
