import qrcode
import base64
import os

def generate_qr_code(inviter_nickname: str, invite_id: uuid.UUID) -> str:
    encoded_data = base64.urlsafe_b64encode(inviter_nickname.encode()).decode()
    qr_data = f"{os.getenv('INVITE_REDIRECT_URL')}?invite={encoded_data}-{invite_id}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    file_path = f"qr_{invite_id}.png"
    img.save(file_path)
    return file_path
