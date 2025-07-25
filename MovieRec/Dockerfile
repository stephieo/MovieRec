FROM python:3.12

COPY . /MovieRec/

WORKDIR /MovieRec

RUN pip install --no-cahe-dir -r requirements.txt

EXPOSE 8000

CMD["python3", "manage.py", "runserver"]