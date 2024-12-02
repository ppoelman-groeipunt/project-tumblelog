from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Hashing password
password = "MySecurePassword"
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
print(f"Original password: {password}")
print(f"Hashed password: {hashed_password}")

# Checking password
input_password = "MySecurePassword"
if bcrypt.check_password_hash(hashed_password, input_password):
    print("Password matches!")
else:
    print("Password does not match!")
