from fastapi import FastAPI, Request, HTTPException
import logging

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Endpoint untuk menerima webhook dari Saweria
@app.post("/webhook")
async def receive_donation(request: Request) -> dict:
    try:
        # Menerima data sebagai dictionary
        data = await request.json()
        
        # Logging data untuk inspeksi
        logging.info(f"Received data: {data}")
        
        return {
            "status": "success",
            "received_data": data
        }
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
