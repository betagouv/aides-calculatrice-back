#!/usr/bin/env bash

all: install api

install:
	poetry install --no-root

api:
	poetry run openfisca serve --country-package openfisca_france

apl:
	curl -X POST http://127.0.0.1:5000/calculate -H 'Content-Type: application/json' -d @payloads/apl.json | jq
