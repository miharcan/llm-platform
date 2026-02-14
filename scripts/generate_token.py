from datetime import datetime, timedelta
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"

payload = {
    "sub": "user1",
    "tenant_id": "acme",
    "role": "admin",
    "exp": datetime.utcnow() + timedelta(hours=1),
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print("Generated JWT:")
print(token)
