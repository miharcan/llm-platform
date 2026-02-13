FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

# 🔥 IMPORTANT LINE
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
    --default-timeout=1000 torch==2.4.0+cpu

# install remaining deps
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
