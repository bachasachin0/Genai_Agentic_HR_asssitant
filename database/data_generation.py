import random
import google.generativeai as genai
from typing import Dict
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

# Define the same lists used in your synthetic data generation
job_titles = [
    "Software Engineer", "Senior Software Engineer", "Data Scientist", "Product Manager",
    "Project Manager", "UX Designer", "QA Engineer", "DevOps Engineer", "CTO", "CEO"
]
departments = [
    "IT", "Engineering", "Data Science", "Product", "Project Management", "Design",
    "Quality Assurance", "Operations", "Executive"
]
office_locations = [
    "Chicago Office", "New York Office", "London Office", "Berlin Office", "Tokyo Office",
    "Sydney Office", "Toronto Office", "San Francisco Office", "Paris Office", "Singapore Office"
]

Currency=["INR","USD","EUR"]

def create_employee_string(employee: Dict) -> str:
    job_details = f"{employee['job_details']['job_title']} in {employee['job_details']['department']}"
    skills = ", ".join(employee['skills'])
    performance_reviews = " ".join([f"Rated {review['rating']} on {review['review_date']}: {review['comments']}" for review in employee['performance_reviews']])
    basic_info = f"{employee['first_name']} {employee['last_name']}, {employee['gender']}, born on {employee['date_of_birth']}"
    work_location = f"Works at {employee['work_location']['nearest_office']}, Remote: {employee['work_location']['is_remote']}"
    notes = employee['notes']

    return f"{basic_info}. Job: {job_details}. Skills: {skills}. Reviews: {performance_reviews}. Location: {work_location}. Notes: {notes}"

def get_embedding(text: str):
    """Generate an embedding for the given text using Google's API."""
    genai.configure(api_key=GOOGLE_API_KEY)
    if not text or not isinstance(text, str):
        return None
    try:
        embeddings = genai.embed_content(model='models/text-embedding-004', content=text, output_dimensionality=768)
        return embeddings['embedding']
    except Exception as e:
        print(f"Error in get_embedding: {e}")
        return None

