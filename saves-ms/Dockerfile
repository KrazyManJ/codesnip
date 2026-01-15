FROM python:3.13-slim

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]