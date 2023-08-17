FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV RUN_TESTS=false

# Use a startup script to determine which command to run
CMD [ "sh", "-c", "if [ \"$RUN_TESTS\" = \"true\" ]; then python test_app.py; else flask run --host=0.0.0.0; fi" ]
