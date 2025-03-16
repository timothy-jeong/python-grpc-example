FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

USER root
RUN apt-get update && \
    apt-get install -y supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

USER root
RUN adduser --disabled-password appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000 50051

# supervisord 설정 파일 복사 (root 권한으로 실행)
USER root
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
USER appuser

CMD ["/usr/bin/supervisord", "-n"]
