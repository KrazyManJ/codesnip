FROM python:3.13-slim

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. search.proto

CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]