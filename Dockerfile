FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

LABEL "org.opencontainers.image.description"="Simple Telegram-bot to create demotivators with your watermark."
LABEL "org.opencontainers.image.source"="https://github.com/timtaran/demotivator-bot"
LABEL "org.opencontainers.image.licenses"="MIT"


RUN apt-get update && apt-get install -y \
    libraqm-dev \
    libfreetype6-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD ./pyproject.toml /app
ADD ./uv.lock /app
RUN uv sync --locked

ADD ./src /app
CMD ["uv", "run", "main.py"]
