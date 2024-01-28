FROM python:3.11-alpine3.19

WORKDIR .

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "main:app", "--reload"]
