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
    qr_path = qrgeneration(inviter.nickname, invite.id)
    qr_url = qrcode_utils(qr_path, "qrcodes", f"invites/{invite.id}.png")
    invite.qr_code_url = qr_url
    db.commit()

    return {"message": "Invite created", "qr_code_url": qr_url}

@router.get("/accept/")
def accept_invite(invite: str, db: Session = Depends(get_db)):
    try:
        inviter_nickname, invite_id = base64.urlsafe_b64decode(invite).decode().split("-")
        invitation = db.query(Invitation).filter(Invitation.id == invite_id).first()
        if not invitation or invitation.status != InvitationStatus.PENDING:
            raise HTTPException(status_code=400, detail="Invalid or expired invitation")

        invitation.mark_accepted()
        db.commit()
        return {"message": "Invitation accepted", "redirect_url": os.getenv("INVITE_REDIRECT_URL")}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid invitation data")
    
@router.get("/invites/")
def get_invites(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    sent_invites = db.query(Invitation).filter(Invitation.inviter_id == user_id).all()
    accepted_count = sum(1 for invite in sent_invites if invite.status == InvitationStatus.ACCEPTED)
    return {"sent": len(sent_invites), "accepted": accepted_count}
