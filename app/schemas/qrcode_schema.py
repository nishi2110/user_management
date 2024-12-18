from pydantic import BaseModel, Field
import uuid

class QRCodeRequest(BaseModel):
    """
    Schema for generating a QR code request.
    """
    inviter_nickname: str = Field(..., max_length=50, description="The nickname of the inviter.")
    invite_id: uuid.UUID = Field(..., description="The unique identifier of the invitation.")

class QRCodeResponse(BaseModel):
    """
    Schema for the response after generating a QR code.
    """
    qr_code_url: str = Field(..., description="The URL of the generated QR code.")
