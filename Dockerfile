FROM python:3.11-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./
RUN uv venv && uv sync --locked

# --- Production stage ---
FROM python:3.11-slim-bookworm

RUN addgroup --system appgroup && adduser --system --group appuser

WORKDIR /app

# Set environment variables and add the virtual environment to the PATH
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" 

# Copy the virtual environment with all dependencies from the builder stage
COPY --from=builder /app/.venv ./.venv

COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]