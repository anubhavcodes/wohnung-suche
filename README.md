### Wohnung suche via Trello
![build status](https://travis-ci.com/anubhavcodes/wohnung-suche.svg?branch=master)

I have been searching for apartments in Germany, and it's not so easy to track the people I have contacted.
I have been using Trello but there is a lot of manual work involved.

This project will help automating most of the things I do. As soon as I create a card and post the url of the apartment
a webhook will be called which scrapes the content from the link and update the card. This is the code for the server responsible
for responding to the webhooks.

### Status

[![asciicast](https://asciinema.org/a/343125.svg)](https://asciinema.org/a/343125)

### Usage

You can use `direnv` to run scripts easily without always needing to use `./scripts/something`

First run:
`./scripts/run-init`
`docker-compose up -d`

Daily development
`docker-compose start`
This will start a development server on port 8005


### Updating requirements.txt
Add your package in `src/requirements.in` and then `./scripts/run-refresh-requirements`.

### Todo

- [x] Integrate sentry.
- [x] Deploy on a cloud provider using self hosted PaaS
- [x] Integrate a CI service like Travis
- [x] Enable continuous deployments.
