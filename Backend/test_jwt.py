from utils.jwt_handler import create_access_token, verify_access_token

payload = {
    "sub": "admin@company.com",
    "role": "Administrator"
}

token = create_access_token(payload)

print("Generated Token:\n")
print(token)

decoded = verify_access_token(token)

print("\nDecoded Payload:")
print(decoded)