FROM python:3.11.0

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

# build args to be passed into container
ARG AOC_SESSION
ARG SLACK_BOT_TOKEN
ARG SLACK_SIGNING_SECRET

ENV AOC_SESSION=${AOC_SESSION}
ENV SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}
ENV SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET}

ENTRYPOINT ["python"]
CMD ["app.py"]