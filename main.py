import os
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException
import logging

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Variabel global untuk menyimpan data
received_data = []

# Get the stream key from environment variable (ensure you set it in Koyeb)
stream_key = os.getenv("STREAM_KEY")

# Function to verify the webhook signature
def verify_signature(data: dict, signature: str) -> bool:
    # Create the HMAC-SHA256 signature using the stream key
    expected_signature = hmac.new(stream_key.encode(), message.encode(), hashlib.sha256).hexdigest()

    # Compare the expected signature with the provided signature
    return hmac.compare_digest(expected_signature, signature)

# Endpoint untuk menerima webhook dari Saweria
@app.post("/webhook")
async def receive_donation(request: Request) -> dict:
    try:
        # Menerima data sebagai dictionary
        data = await request.json()
        
        # Logging data untuk inspeksi
        logging.info(f"Received data: {data}")
        
        # Get the signature from the request headers (assuming it's passed)
        signature = request.headers.get("X-Saweria-Signature")

        # Verify the signature
        if signature is None or not verify_signature(data, signature):
            logging.error("Invalid signature")
            raise HTTPException(status_code=400, detail="Invalid signature")

        # Simpan data yang diterima
        received_data.append(data)
        
        return {
            "status": "success",
            "received_data": data
        }
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Endpoint untuk menampilkan data dalam JSON
@app.get("/show-data")
async def show_data() -> dict:
    return {"received_data": received_data}
