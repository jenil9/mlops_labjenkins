FROM python:3.12-slim

# Force Python logs to stream directly to the terminal without buffering
ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "appfile.py"]

# Multi-stage:

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
# RUN pip install --no-cache-dir --find-links=/wheels -r requirements.txt && rm -rf /wheels
# COPY appfile.py model_train.py iris_model.pkl ./
# COPY templates ./templates
# EXPOSE 5001
# CMD ["python", "appfile.py"]