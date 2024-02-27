# generate_test_token.py
from jwt_handler import generate_token, verify_token

test_user_id = "144"  
test_user_name = "Yashwanth"
test_user_nickname = "Yash"

token = generate_token(test_user_id, test_user_name, test_user_nickname)
print("Generated JWT Token:", token)

