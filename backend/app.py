"""FastAPI application entry-point for IrrigaBot backend.

This minimal scaffold will expand as additional routes and business logic are implemented.
"""
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI(title="IrrigaBot API", version="0.1.0")


@app.get("/health", summary="Health check", tags=["meta"])
async def health_check() -> JSONResponse:
    """Return simple service liveliness indicator.

    Returns
    -------
    JSONResponse
        `{ "status": "ok" }` with HTTP 200.
    """
    return JSONResponse({"status": "ok"}, status_code=status.HTTP_200_OK)