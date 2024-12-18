import qrcode
import base64
import os
import uuid
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the directory to save QR codes
QR_CODE_DIRECTORY = "static/qr_codes"
Path(QR_CODE_DIRECTORY).mkdir(parents=True, exist_ok=True)

def generate_qr_code(inviter_nickname: str, invite_id: uuid.UUID) -> str:
    """
    Generates a QR code for an invitation.

    Args:
        inviter_nickname (str): The nickname of the inviter.
        invite_id (uuid.UUID): The unique identifier of the invitation.

    Returns:
        str: The file path of the saved QR code image.
    """
    # Base64 encode the inviter nickname
    encoded_nickname = base64.urlsafe_b64encode(inviter_nickname.encode()).decode()
    
    # Construct the QR code data with the encoded nickname and invite ID
    invite_redirect_url = os.getenv("INVITE_REDIRECT_URL", "http://example.com/invite")
    qr_data = f"{invite_redirect_url}?invite={encoded_nickname}-{invite_id}"
    
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # Version of the QR code (size)
        box_size=10,  # Size of each box in the QR code
        border=4,  # Border size of the QR code
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Generate the QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the QR code image to the specified directory
    file_path = os.path.join(QR_CODE_DIRECTORY, f"qr_{invite_id}.png")
    img.save(file_path)

    return file_path
