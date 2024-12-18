from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.services.qrcode_service import QRCodeService
from app.schemas.qrcode_schema import QRCodeRequest, QRCodeResponse

router = APIRouter()

@router.post("/", response_model=QRCodeResponse, tags=["QR Codes"])
async def generate_qr_code(data: QRCodeRequest, db: AsyncSession = Depends(get_db)):
    """
    Generate a QR code.
    """
    qr_code_url = await QRCodeService.generate_qr_code(db, data.dict())
    if qr_code_url:
        return QRCodeResponse(qr_code_url=qr_code_url)
    raise HTTPException(status_code=500, detail="Failed to generate QR code")
