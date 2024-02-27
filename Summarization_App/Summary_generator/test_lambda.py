import json
from summarize_api import lambda_handler  # Replace 'your_lambda_file' with the name of your Python file containing lambda_handler

# Simulate Lambda event
event = {
    "headers": {
        "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImV4cCI6MTcwODkzNDQ3NX0.eB0QreuSudngDTKUn9bEPKM6TxfoGK_fi3jzEIk_-Zk"
    },
    "body": json.dumps({
        "description": '''Pfizer is backing the American Cancer Society’s (ACS') work to address disparities in oncology outcomes, providing $15 million over three years to boost efforts to connect people to no- and low-cost screening opportunities.
The ACS has identified limited access to quality healthcare in certain communities, including people of color and people living in rural areas, as barriers to its goal of “ending cancer as we know it.” In breast cancer, Black women are twice as likely to be diagnosed at a later stage and have a 40% higher mortality rate than white women. Black men are twice as likely to die from prostate cancer than white men.
Seeking to close the gaps, the ACS and Pfizer have partnered on “Change the Odds: Uniting to Improve Cancer Outcomes.” The new, three-year initiative is intended to “make a tangible, sustainable difference in communities that are disproportionately impacted by cancer, but medically underserved,” ACS CEO Karen Knudsen said in a Q&A published by Pfizer.
Knudsen said the ACS will “connect individuals and promote awareness of no- and low-cost screening opportunities” with a view to “[reaching] people where they are with these services and [linking] them to appropriate follow-up and support.” The $15 million from Pfizer will help “amplify our ongoing screening efforts and hopefully make a significant impact in these communities,” the ACS CEO added.
''',
        "points_words": 5,
        "Summary_type": "pointers",
        "importance": "NSCLC",
        "exclude": "NUMBERS",
        "additional_info": "END WITH XYZ"
    })
}
context = {}

if __name__ == "__main__":
    try:
        response = lambda_handler(event, context)
        print("Lambda Response:", response)
    except Exception as e:
        print("Error during lambda invocation:", e)

