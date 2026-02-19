"""
PL202 — Serverless Event Processing (Local Lambda Simulation)
Day 1 (45 min) — Individual Task

You will implement a Lambda-style handler:
    def handler(event, context): -> dict

Requirements (high level):
- Validate event structure
- Normalize important fields
- Return a JSON-serializable dict with:
    status: "ok" or "error"
    message: short explanation
    data: normalized data OR None
    errors: list of strings (only when status="error")

Event types you must support:
- USER_SIGNUP
- PAYMENT
- FILE_UPLOAD

Run locally:
    python run_local.py --event events/01_user_signup_valid.json
    python run_local.py --all
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
import re


ALLOWED_TYPES = {"USER_SIGNUP", "PAYMENT", "FILE_UPLOAD"}


def _err(*msgs: str) -> Dict[str, Any]:
    """Create a standard error response."""
    return {
        "status": "error",
        "message": "Event rejected",
        "data": None,
        "errors": list(msgs),
    }


def _ok(message: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a standard ok response."""
    return {
        "status": "ok",
        "message": message,
        "data": data,
        "errors": [],
    }


def _is_email(value: str) -> bool:
    # Simple email check (good enough for class)
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))


def handler(event: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Main Lambda-style handler."""
    # TODO 1: Validate event is a dict and has 'type' field
    # TODO 2: Ensure event['type'] is one of ALLOWED_TYPES
    # TODO 3: Route to a per-type function:
    #         - handle_user_signup(event)
    #         - handle_payment(event)
    #         - handle_file_upload(event)
    # TODO 4: Return the dict response from the handler function

    if not isinstance(event, dict):
        return _err("Event must be a dictionary")

    event_type = event.get("type")
    if not event_type:
        return _err("Missing event type")

    if event_type not in ALLOWED_TYPES:
        return _err(f"Unsupported event type: {event_type}")

    if event_type == "USER_SIGNUP":
        return handle_user_signup(event)
    elif event_type == "PAYMENT":
        return handle_payment(event)
    elif event_type == "FILE_UPLOAD":
        return handle_file_upload(event)

    return _err("Unhandled event type")


def handle_user_signup(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process USER_SIGNUP events."""
    # Required fields:
    # - user_id (int)
    # - email (str)
    # - plan (str) one of: free, pro, edu
    #
    # Normalization:
    # - email -> lowercase
    # - plan -> lowercase
    #
    # Output data should include:
    # - user_id, email, plan, welcome_email_subject
    #
    # TODO 5: Validate required fields and types
    # TODO 6: Validate email format with _is_email
    # TODO 7: Validate plan is allowed
    # TODO 8: Build normalized output data and return _ok(...)

    required = ["user_id", "email", "plan"]
    for field in required:
        if field not in event:
            return _err(f"Missing field: {field}")

    user_id = event["user_id"]
    email = event["email"]
    plan = event["plan"]

    if not isinstance(user_id, int):
        return _err("user_id must be int")

    if not isinstance(email, str) or not _is_email(email):
        return _err("Invalid email")

    if not isinstance(plan, str):
        return _err("plan must be string")

    plan = plan.lower()
    if plan not in {"free", "pro", "edu"}:
        return _err("Invalid plan")

    email = email.lower()

    data = {
        "user_id": user_id,
        "email": email,
        "plan": plan,
        "welcome_email_subject": f"Welcome to the {plan} plan!"
    }

    return _ok("Signup processed", data)


def handle_payment(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process PAYMENT events."""
    # Required fields:
    # - payment_id (str)
    # - user_id (int)
    # - amount (float or int) must be > 0
    # - currency (str) allowed: BHD, USD, EUR
    #
    # Normalization:
    # - currency -> uppercase
    # - amount -> float rounded to 3 decimals
    #
    # Output data should include:
    # - payment_id, user_id, amount, currency, fee, net_amount
    #   where fee = 2% of amount (0.02 * amount), net_amount = amount - fee
    #
    # TODO 9: Validate required fields and types
    # TODO 10: Validate amount > 0
    # TODO 11: Validate currency allowed
    # TODO 12: Compute fee and net_amount and return _ok(...)

    required = ["payment_id", "user_id", "amount", "currency"]
    for field in required:
        if field not in event:
            return _err(f"Missing field: {field}")

    payment_id = event["payment_id"]
    user_id = event["user_id"]
    amount = event["amount"]
    currency = event["currency"]

    if not isinstance(payment_id, str):
        return _err("payment_id must be string")

    if not isinstance(user_id, int):
        return _err("user_id must be int")

    if not isinstance(amount, (int, float)):
        return _err("amount must be number")

    if amount <= 0:
        return _err("amount must be greater than 0")

    if not isinstance(currency, str):
        return _err("currency must be string")

    currency = currency.upper()
    if currency not in {"BHD", "USD", "EUR"}:
        return _err("Invalid currency")

    amount = round(float(amount), 3)
    fee = round(amount * 0.02, 3)
    net_amount = round(amount - fee, 3)

    data = {
        "payment_id": payment_id,
        "user_id": user_id,
        "amount": amount,
        "currency": currency,
        "fee": fee,
        "net_amount": net_amount
    }

    return _ok("Payment processed", data)


def handle_file_upload(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process FILE_UPLOAD events."""
    # Required fields:
    # - file_name (str)
    # - size_bytes (int) must be >= 0
    # - bucket (str)
    # - uploader (str) (email)
    #
    # Normalization:
    # - bucket -> lowercase
    # - file_name -> strip spaces
    # - uploader -> lowercase
    #
    # Output data should include:
    # - file_name, size_bytes, bucket, uploader, storage_class
    #
    # Storage class rules:
    # - size_bytes < 1_000_000  -> "STANDARD"
    # - size_bytes < 50_000_000 -> "STANDARD_IA"
    # - otherwise              -> "GLACIER"
    #
    # TODO 13: Validate required fields and types
    # TODO 14: Validate uploader email
    # TODO 15: Compute storage_class and return _ok(...)

    required = ["file_name", "size_bytes", "bucket", "uploader"]
    for field in required:
        if field not in event:
            return _err(f"Missing field: {field}")

    file_name = event["file_name"]
    size_bytes = event["size_bytes"]
    bucket = event["bucket"]
    uploader = event["uploader"]

    if not isinstance(file_name, str):
        return _err("file_name must be string")

    if not isinstance(size_bytes, int) or size_bytes < 0:
        return _err("size_bytes must be non-negative integer")

    if not isinstance(bucket, str):
        return _err("bucket must be string")

    if not isinstance(uploader, str) or not _is_email(uploader):
        return _err("Invalid uploader email")

    file_name = file_name.strip()
    bucket = bucket.lower()
    uploader = uploader.lower()

    if size_bytes < 1_000_000:
        storage_class = "STANDARD"
    elif size_bytes < 50_000_000:
        storage_class = "STANDARD_IA"
    else:
        storage_class = "GLACIER"

    data = {
        "file_name": file_name,
        "size_bytes": size_bytes,
        "bucket": bucket,
        "uploader": uploader,
        "storage_class": storage_class
    }

    return _ok("Upload processed", data)
