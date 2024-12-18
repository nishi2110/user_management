from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import QRCode  # Ensure the QRCode model exists
from app.utils.qrgeneration import generate_qr_code  # Ensure the utility exists

class QRCodeService:
    @staticmethod
    async def generate_qr_code(db: AsyncSession, data: dict) -> str:
        """
        Generates a QR code URL for the provided data and saves it to the database.

        Args:
            db (AsyncSession): The database session.
            data (dict): Data for the QR code.

        Returns:
            str: URL of the generated QR code.
        """
        qr_code_image_url = generate_qr_code_image(data)

        # Save the QR code data to the database (example)
        qr_code_entry = QRCode(
            data=data,
            qr_code_url=qr_code_image_url,
        )
        db.add(qr_code_entry)
        await db.commit()

        return qr_code_image_url
