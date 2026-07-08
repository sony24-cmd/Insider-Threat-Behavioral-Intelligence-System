from utils.password import hash_password, verify_password

password = "Admin@123"

hashed = hash_password(password)

print("Original Password :", password)
print("Hashed Password   :", hashed)

print("Verification (Correct):", verify_password(password, hashed))
print("Verification (Wrong):", verify_password("WrongPassword", hashed))