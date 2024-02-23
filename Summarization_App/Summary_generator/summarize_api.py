
import os
import asyncio
import traceback
from dotenv import load_dotenv
from Summary_engine.summarization_var import Summarizer_var
from Summary_engine.classification import Categorizer
from Summary_engine.utilities import log_error, log_info, log_error, log_info, handle_errors
from preprocessing.content_preprocessing import TextPreprocessor
from config import Classification_Config
import json
import pandas as pd
import datetime
from jwt_handler import verify_token


# Assuming AWS Lambda environment variables are set for any needed configuration
load_dotenv()

@handle_errors
async def summarize(description, points_words, Summary_type, importance, exclude, additional_info):
    try:
        description = description.strip()
        Summary_type = Summary_type.lower() # type: ignore
        SummarizerVar = Summarizer_var()
        if Summary_type == "pointers":
            summary = await SummarizerVar.process_description(
                description, points_words=points_words, Summary_type=Summary_type, exclude=exclude, importance=importance, additional_info=additional_info
            )
        elif Summary_type == "paragraph":
            points_words = f"{points_words} words"
            summary = await SummarizerVar.process_description(
                description, points_words=points_words, Summary_type=Summary_type, exclude=exclude, importance=importance, additional_info=additional_info
            )
        else:
            # Handling unsupported cases or default behavior
            raise ValueError("Unsupported Summary_type")

        return {"description": description, "summary": summary}
    
    except ValueError as ve:
        log_error(f"Invalid input: {str(ve)}")
        return {"error": "Invalid input. Check your request payload."}

    except Exception as e:
        log_error(f"Error processing summary: {str(e)}")
        return {"error": "Internal Server Error. Contact the administrator."}

def lambda_handler(event, context):
    # Attempt to extract the token from the Authorization header
    token = event.get('headers', {}).get('Authorization')
    if not token or not verify_token(token):  # verify_token should return False if the token is invalid
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Unauthorized. Invalid or missing token."})
        }
    # Parse input data from event
    try:
        data = event.get('body')  # Assuming event['body'] contains the input JSON as a string
        if isinstance(data, str):
            data = json.loads(data)
        
        description = data.get('description', '')
        points_words = data.get('points_words', 0)
        Summary_type = data.get('Summary_type', '')
        importance = data.get('importance', '')
        exclude = data.get('exclude', '')
        additional_info = data.get('additional_info', '')
        
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(summarize(description, points_words, Summary_type, importance, exclude, additional_info))
        
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        log_error(f"Unhandled exception: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error. Please try again later."})
        }












































# import os
# import asyncio
# import traceback
# from dotenv import load_dotenv
# from Summary_engine.summarization_var import Summarizer_var
# from Summary_engine.classification import Categorizer
# from Summary_engine.utilities import log_error, log_info
# from preprocessing.content_preprocessing import TextPreprocessor
# from config import Classification_Config
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import pandas as pd
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import datetime

 
# app = FastAPI()

# class SummaryRequest(BaseModel):
#     description: str = ""
#     additional_info: str = ""
#     points_words: int
#     Summary_type: str 
#     importance: str = ""
#     exclude: str = ""

# @app.post("/summarize")
# async def summarize(data: SummaryRequest):
#     try:
#         description = data.description.strip()
#         points_words = data.points_words
#         Summary_type= data.Summary_type.lower() # type: ignore
#         importance = data.importance
#         exclude = data.exclude
#         additional_info= data.additional_info


#         SummarizerVar = Summarizer_var()
#         if Summary_type == "pointers":
#             summary = await SummarizerVar.process_description(
#                 description, points_words=points_words, Summary_type=Summary_type, exclude=exclude, importance=importance, additional_info=additional_info
#             )
#         elif Summary_type == "paragraph":
#             points_words = f"{points_words} words"
#             # Using a default value for points_words for paragraphs
#             summary = await SummarizerVar.process_description(
#                 description, points_words=points_words, Summary_type=Summary_type, exclude=exclude, importance=importance, additional_info=additional_info
#             )
#         else:
#             # Handling unsupported cases or and default behavior
#             return HTTPException(status_code=422, detail="Unsupported Summary_type")

#         return {"description": description, "summary": summary}
    
#     except ValueError as ve:
#         log_error(f"Invalid input: {str(ve)}")
#         raise HTTPException(status_code=422, detail="Invalid input. Check your request payload.")

#     except HTTPException as he:
#         raise

#     except Exception as e:
#         log_error(f"Error processing summary: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error. Contact the administrator.")

   
# app.post("/")
# async def home(data: SummaryRequest):
#     return {
#         ""
#         }

# load_dotenv()


# class Summarizer:
#     def __init__(self, link) -> None:
#         self.link = link
#         self.store_data()
#         row = self.filter_link_records()
#         self.description = self.get_description(row)
    
#     def store_data(self):
#         input_excel_file = os.getenv("INPUT_EXCEL_FILE")
#         self.df = ExcelHandler.read_excel(input_excel_file)

#     def filter_link_records(self):
#         return self.df.loc[self.df['LINK'].astype(str).str.strip() == self.link.strip()]
   
    
#     def get_description(self, row) -> str:
#         return f"Title: {row['TITLE'].values[0]} Description: {row['DESCRIPTION'].values[0]}"

# class Cat:
#     def __init__(self, link) -> None:
#         self.link = link
#         self.store_data()
#         row = self.filter_link_records()
#         self.description = self.get_description(row)
    
#     def store_data(self):
#         input_excel_file = os.getenv("INPUT_EXCEL_FILE")
#         self.df = ExcelHandler.read_excel(input_excel_file)

#     def filter_link_records(self):
#         return self.df.loc[self.df['LINK'].astype(str).str.strip() == self.link.strip()]
   
    
#     def get_description(self, row) -> str:
#         return f"Title: {row['TITLE'].values[0]} Description: {row['DESCRIPTION'].values[0]}"



    # async def summarize_content(self, link, words=30, importance="", exclude="default_exclude"):
    #     try:
    #         task_type = "summarization_var"
    #         input_excel_file = os.getenv("INPUT_EXCEL_FILE")
    #         df = ExcelHandler.read_excel(input_excel_file)
    #         stripped_link = link.strip()
    #         categorized_content = await self.preprocess_and_categorize_by_link(df, stripped_link, task_type, df['MATCHD_KEYWRD'].iloc[0])

    #         if categorized_content is not None:
    #             print(f"Summarized Content for link {stripped_link}:")
    #             print(categorized_content)
    #         else:
    #             log_info("No content to summarize.")
    #     except Exception as e:
    #         log_error(f"Error in summarize_content: {e}")
    #         log_error(traceback.format_exc())
            # log_info(f"No rows found for the link: {link}")
            # return None

    


#     async def preprocess_text(self, text):
#         return await asyncio.to_thread(TextPreprocessor.preprocess_text, text)

# def process(link, words=30, importance="", exclude="default_exclude"):
#     summarizer = Summarizer()
#     description = asyncio.run(summarizer.get_description(link))
#     asyncio.run(summarizer.summarize_content(link, words, importance, exclude))
#     return {
#         "description": description,
#         "summary": "Summary"
#     }

# if __name__ == "__main__":
#     try:
#         link = input("Enter link: ").strip()
#         result = process(link)
#         print(result)
#     except Exception as e:
#         log_error(f"Error in main execution: {e}")
