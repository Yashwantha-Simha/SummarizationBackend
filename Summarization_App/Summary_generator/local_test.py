import json
from jwt_handler import generate_token
from summarize_api import lambda_handler

def generate_test_token():
    test_user_id = 123  # Example user ID
    return generate_token(test_user_id)

def create_lambda_event(token, body):
    return {
        "headers": {
            "authorization": f"Bearer {token}"
        },
        "body": json.dumps(body)
    }

def main():
    token = generate_test_token()
    print(f"Generated JWT Token: {token}")

    test_body = {
        "description": "Pfizer is backing the American Cancer Society’s (ACS') work to address disparities in oncology outcomes, providing $15 million over three years to boost efforts to connect people to no- and low-cost screening opportunities.\nThe ACS has identified limited access to quality healthcare in certain communities, including people of color and people living in rural areas, as barriers to its goal of “ending cancer as we know it.” ",
    "points_words": 5,
    "Summary_type": "pointers",
    "importance": "NSCLC",
    "exclude": "NUMBERS",
    "additional_info": "END WITH XYZ"
    }
 
    event = create_lambda_event(token, test_body)
    response = lambda_handler(event, {})
    print("Lambda Handler Response:", response)

if __name__ == "__main__":
    main()
