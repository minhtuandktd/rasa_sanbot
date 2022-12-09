FROM python:3.9.13

WORKDIR /usr/src

COPY . .

RUN apt-get update
RUN pip install -r requirements.txt

# run command
CMD ["rasa", "run" , "--enable-api", "--port", "5005"]