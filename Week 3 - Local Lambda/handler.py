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
    return _err("TODO: handler not implemented")


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
    return _err("TODO: handle_user_signup not implemented")


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
    return _err("TODO: handle_payment not implemented")


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
    return _err("TODO: handle_file_upload not implemented")
