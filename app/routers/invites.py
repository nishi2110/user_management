from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, Invitation
from app.utils import qrgeneration, qrcode_utils

router = APIRouter()

@router.post("/invite/")
def create_invite(
    inviter_id: uuid.UUID,
    invitee_name: str,
    invitee_email: str,
    db: Session = Depends(get_db)
):
    inviter = db.query(User).filter(User.id == inviter_id).first()
    if not inviter:
        raise HTTPException(status_code=404, detail="Inviter not found")

    invite = Invitation(
        inviter_id=inviter_id,
        invitee_name=invitee_name,
        invitee_email=invitee_email,
    )
    db.add(invite)
    db.commit()
    db.refresh(invite)

    # Generate and upload QR Code
    qr_path = generate_qr_code(inviter.nickname, invite.id)
    qr_url = upload_to_minio(qr_path, "qrcodes", f"invites/{invite.id}.png")
    invite.qr_code_url = qr_url
    db.commit()

    return {"message": "Invite created", "qr_code_url": qr_url}