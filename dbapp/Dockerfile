FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5002

CMD ["python", "app.py"]

# Multi-stage 
# FROM python:3.12-slim AS builder
# WORKDIR /build
# COPY requirements.txt .
# RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt
#
# FROM python:3.12-slim AS runtime
# ENV PYTHONUNBUFFERED=1
# WORKDIR /app
# COPY requirements.txt .
# COPY --from=builder /wheels /wheels
# RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && rm -rf /wheels
# COPY app.py .
# EXPOSE 5002
# CMD ["python", "app.py"]