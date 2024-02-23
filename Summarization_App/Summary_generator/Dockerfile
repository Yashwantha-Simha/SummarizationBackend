
# Use an official Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.11

COPY . /var/task

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD ["summarize_api.lambda_handler"]

