FROM python:3.12-slim

WORKDIR /app

# Copy files
COPY core/ /app/core/
COPY static/ /app/static/
COPY server.py cli.py main.py requirements.txt /app/

RUN mkdir -p /app/data /app/export

EXPOSE 8088

CMD ["python", "main.py", "serve", "--host", "0.0.0.0", "--port", "8088"]
