FROM python:3.11-alpine

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn","app:app","--host","0.0.0.0"]