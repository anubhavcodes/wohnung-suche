### Wohnung suche via Trello

I have been searching for apartments in Germany, and it's not so easy to track the people I have contacted.
I have been using Trello but there is a lot of manual work involved.

This project will help automating most of the things I do. As soon as I create a card and post the url of the apartment
a webhook will be called which scrapes the content from the link and update the card. This is the code for the server responsible
for responding to the webhooks.

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

- [ ] Integrate sentry.
