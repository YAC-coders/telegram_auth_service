FROM python:3.13.5-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    WORKDIR_PATH="/app" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

ENV PATH="$WORKDIR_PATH/.venv/bin:$PATH"

WORKDIR $WORKDIR_PATH


FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:0.8.3 /uv /uvx /bin/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM base AS final

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean

COPY --from=builder --chown=$PYSETUP_PATH:$PYSETUP_PATH $WORKDIR_PATH $WORKDIR_PATH

CMD ["python", "src/main.py"]
