"""Unit tests for the security helpers."""

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hashing_roundtrip():
    hashed = hash_password("s3cret")
    assert hashed != "s3cret"
    assert verify_password("s3cret", hashed)
    assert not verify_password("nope", hashed)


def test_jwt_roundtrip():
    token = create_access_token("user@example.com")
    assert decode_access_token(token) == "user@example.com"


def test_jwt_invalid_token():
    assert decode_access_token("not-a-real-token") is None
