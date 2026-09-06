"""
Vercel serverless entrypoint.

Vercel's Python runtime auto-detects an ASGI app exported as `app` from any file
under /api and wraps it in its own request handler - no extra adapter needed.
This just re-exports the existing FastAPI app so the same codebase that runs in
Docker (see Dockerfile / docker-compose.yml) also serves the live demo.
"""
from stockai.server import app  # noqa: F401
