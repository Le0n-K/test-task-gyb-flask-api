FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off


RUN python -m pip install --upgrade pip && \
    pip install poetry

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

EXPOSE 5000

CMD ["python", "main.py"]