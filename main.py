import os
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, Depends
import logging

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Stream key from environment variable
stream_key = os.environ.get("STREAM_KEY")
if not stream_key:
    raise ValueError("STREAM_KEY environment variable is not set.")

# Function to generate HMAC-SHA256 signature
def verify_signature(received_signature: str, data_string: str, key: str) -> bool:
    """
    Verifies the HMAC-SHA256 signature.
    """
    generated_hmac = hmac.new(key.encode(), data_string.encode(), hashlib.sha256).hexdigest()
    logging.info(f"Generated HMAC: {generated_hmac}")
    try:
        return hmac.compare_digest(generated_hmac, received_signature)
    except Exception as e:
        logging.error(f"Error comparing signatures: {e}")
        return False

# Middleware-like dependency for signature verification
async def verify_saweria_signature(request: Request):
    # Get signature from headers
    signature = request.headers.get("Saweria-Callback-Signature")
    if not signature:
        logging.error("Missing Saweria-Callback-Signature header.")
        raise HTTPException(status_code=403, detail="Missing signature header.")

    # Read raw request body
    raw_body = await request.body()
    logging.info(f"Raw body: {raw_body}")
    logging.info(f"Received signature: {signature}")

    # Prepare the data string (concatenate required fields)
    try:
        payload = await request.json()  # Parse JSON to get payload fields
        data_string = f"{payload['version']}{payload['id']}{payload['amount_raw']}{payload['donator_name']}{payload['donator_email']}"
    except Exception as e:
        logging.error(f"Failed to parse payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload format.")

    # Verify the signature
    if not verify_signature(signature, data_string, stream_key):
        print(signature)
        print(data_string)
        print(stream_key)
        logging.error("Invalid signature.")
        raise HTTPException(status_code=401, detail="Invalid signature.")

# Global variable to store received data
received_data = []

# Endpoint to handle Saweria webhook
@app.post("/webhook")
async def receive_donation(
    request: Request,
    _: None = Depends(verify_saweria_signature)
) -> dict:
    try:
        # Parse JSON body after verification
        data = await request.json()
        logging.info("Verified donation data: %s", data)

        # Store the data in the global list
        received_data.append(data)

        return {"status": "success", "data": data}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Endpoint to display received data
@app.get("/show-data")
async def show_data():
    return {"received_data": received_data}
