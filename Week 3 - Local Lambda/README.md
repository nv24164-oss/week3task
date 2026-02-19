# week3task
# Week 3 — Serverless Event Processing

## Overview
This project simulates a serverless Lambda function that processes cloud events. It supports three types of events:

- **USER_SIGNUP** — validates user data, normalizes email and plan, returns a welcome message.
- **PAYMENT** — validates payment details, normalizes currency, calculates fee and net amount.
- **FILE_UPLOAD** — validates file upload data, normalizes names, assigns a storage class based on file size.

## Files
- `handler.py` — contains the main Lambda handler and per-event functions.
- `run_local.py` — script to run events locally.
- `events/` — sample JSON events (valid + invalid).
- `expected_outputs/` — expected outputs for valid events.
- `run_proof.txt` — output from running `python run_local.py --all`.

## Usage
Run all events locally:

```bash
python run_local.py --all
