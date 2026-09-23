import re

def validate_registration(email: str) -> bool:
    # QUAL: duplicated regex — same pattern repeated below
    pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    return bool(pattern.match(email))

def validate_contact(email: str, phone: str) -> dict:
    # QUAL: same email regex duplicated here instead of reusing helper
    pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    return {
        "email_ok": bool(pattern.match(email)),
        "phone_ok": bool(phone and phone.isdigit() and len(phone) >= 7),
    }
