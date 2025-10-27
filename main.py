from user_service.src.utils import create_token, decode_token



token = create_token(1, "admin")

print(token)
print(decode_token(token))

