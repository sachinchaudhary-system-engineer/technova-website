
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
ENV DATA_DIR=/data

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY app.py .

RUN useradd --system --uid 10001 --no-create-home appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /app /data

USER 10001:10001

EXPOSE 5000

CMD ["python", "app.py"]
