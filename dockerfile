FROM python:3.11

COPY requirements.txt /

RUN pip install -r /requirements.txt

EXPOSE 8000

COPY . / 

CMD ["hypercorn", "run:app", "-b", "0.0.0.0:8000"]
