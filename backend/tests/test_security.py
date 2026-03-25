from app.core.security import generate_access_key, generate_case_id, hash_access_key, verify_access_key


def test_case_id_format() -> None:
    case_id = generate_case_id()
    assert case_id.startswith("CASE-")
    assert len(case_id.split("-")) == 3


def test_access_key_hash_roundtrip() -> None:
    access_key = generate_access_key()
    hashed = hash_access_key(access_key)
    assert verify_access_key(access_key, hashed)

