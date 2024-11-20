import os
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, Depends
import logging

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Stream key from environment variable
stream_key = {{ STREAM_KEY }}
if not stream_key:
    raise ValueError("STREAM_KEY environment variable is not set.")

# Middleware-like dependency for signature verification
def verify_saweria_signature(stream_key: str):
    async def dependency(request: Request):
        # Get signature from headers
        signature = request.headers.get("Saweria-Callback-Signature")
        if not signature:
            logging.error("Missing Saweria-Callback-Signature header.")
            raise HTTPException(status_code=403, detail="Missing signature header.")

        # Read raw request body
        raw_body = await request.body()

        # Generate HMAC-SHA256 signature using stream key
        expected_signature = hmac.new(
            stream_key.encode(),
            raw_body,
            hashlib.sha256
        ).hexdigest()

        # Compare signatures
        if not hmac.compare_digest(expected_signature, signature):
            logging.error("Invalid signature.")
            raise HTTPException(status_code=401, detail="Invalid signature.")
    return dependency

# Add the signature verification as a dependency
verify_signature = verify_saweria_signature(stream_key)

# Endpoint to handle Saweria webhook
@app.post("/webhook")
async def receive_donation(
    request: Request,
    _: None = Depends(verify_signature)
) -> dict:
    try:
        # Parse JSON body after verification
        data = await request.json()
        logging.info("Verified donation data: %s", data)

        return {"status": "success", "data": data}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/show-data")
async def show_data():
    return {"received_data": received_data}
