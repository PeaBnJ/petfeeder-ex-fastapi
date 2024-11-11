from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# Membuat model untuk data yang akan dikirim oleh Saweria (contoh data donasi)
class DonationData(BaseModel):
    amount: int
    username: str
    message: str
    transaction_id: str

# Endpoint untuk menerima webhook dari Saweria
@app.post("/webhook")
async def receive_donation(data: DonationData):
    # Proses data donasi yang diterima
    print(f"Donasi diterima: {data.amount} dari {data.username}")
    print(f"Pesan: {data.message}")
    print(f"Transaction ID: {data.transaction_id}")

    # Anda bisa menambahkan logika lain di sini, seperti menambahkan notifikasi, memperbarui UI, dll.
    return {"status": "success"}
