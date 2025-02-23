#!/usr/bin/env bash

GREEN := '\033[0;32m'
COLOR_OFF := '\033[0m'
POETRY_CURRENT_ENV_PATH := $(shell poetry env info -p)


all: install api

install:
	@echo $(GREEN)"Using virtualenv: "$(POETRY_CURRENT_ENV_PATH)$(COLOR_OFF)
	poetry install

api:
	poetry run openfisca serve --country-package openfisca_france

apl:
	curl -X POST http://127.0.0.1:5000/calculate -H 'Content-Type: application/json' -d @payloads/apl.json | jq

apl+d:
	curl -X POST http://127.0.0.1:5000/calculate -H 'Content-Type: application/json' -d @payloads/apl_debug.json | jq
