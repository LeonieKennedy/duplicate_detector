FROM python:3.8
RUN apt update && apt full-upgrade -y
RUN apt install -y git

WORKDIR /app
# Install base utilities
RUN apt update && \
    apt install -y build-essential  && \
    apt install -y wget && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*


COPY . .

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
