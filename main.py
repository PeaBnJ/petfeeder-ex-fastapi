from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, ValidationError
from datetime import datetime
import logging

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Model untuk data yang akan dikirim oleh Saweria (contoh data donasi)
class DonationNotification(BaseModel):
    version: str
    created_at: datetime
    id: str
    type: str
    amount_raw: int
    cut: int
    donator_name: str
    donator_email: str
    donator_is_user: bool
    message: str

# Endpoint untuk menerima webhook dari Saweria
@app.post("/webhook")
async def receive_donation(data: DonationNotification) -> dict:
    try:
        # Validasi data
        data = DonationNotification(**data.dict())
        
        # Logging data
        logging.info(f"Received donation: {data.dict()}")
        
        # Proses data
        return {
            "notification_body": data.dict(),
            "esp32_status": "Success"
        }
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail="Invalid data")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
