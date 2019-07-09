FROM python:3.6-slim

# Put require here to use cached layers when possible
ADD requirements.txt /tmp/requirements.txt
RUN pip install --trusted-host pypi.python.org -r /tmp/requirements.txt

WORKDIR /app

COPY . /app

EXPOSE 5000

ENV FLASK_APP app.py

CMD ["flask", "run", "--host=0.0.0.0"]
