from fastapi import FastAPI
from rpc import get_tx, get_receipt, w3
from decorder import decode_transfers
from explain import explain
from gemini_explain import gemini_explain
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/tx/{tx_hash}")
def analyze(tx_hash: str):

    tx = get_tx(tx_hash)
    receipt = get_receipt(tx_hash)
    transfers = decode_transfers(receipt, w3)

    # Structured machine-readable explanation (your existing logic)
    structured = explain(tx, transfers)

    # Plain-English explanation powered by Gemini
    human_readable = gemini_explain(structured, transfers)

    return {
        "human_explanation": human_readable,   # ← Gemini output (show this to users)
        "structured":        structured,        # ← your original output (keep for debugging)
        "transfers":         transfers
    }
