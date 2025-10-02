from app.core.security import (
    generate_api_key,
    generate_random_code,
    get_password_hash,
    verify_password,
)


def test_generate_random_code():
    default_num_characters = 8
    result = generate_random_code()
    print(result)
    assert len(result) == default_num_characters


def test_generate_random_code_32_caracters():
    num_characters = 32
    result = generate_random_code(num_characters)
    print(result)
    assert len(result) == num_characters


def test_generate_api_key():
    default_lenght = 72
    prefix_api_key = "api_key_"
    result = generate_api_key()
    assert result.startswith(prefix_api_key)
    assert len(result) == default_lenght


def test_get_password_hash_and_verify_password():
    password = "test"
    password_hash = get_password_hash(password)
    assert verify_password(password, password_hash)
