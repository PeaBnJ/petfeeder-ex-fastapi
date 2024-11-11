from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

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
    # Menampilkan data yang diterima di console
    return {
        "notification_body": data.dict(),
        "esp32_status": "Success"
    }
