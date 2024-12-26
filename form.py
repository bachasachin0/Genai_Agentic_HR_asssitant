import streamlit as st
import os
from database.data_generation import create_employee_string, get_embedding, Currency,job_titles,departments,office_locations
from database.db_connection import get_mongo_client, push_data_to_mongo
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# CSS for form styling
form_css = """
    <style>
        .form-container {
            border: 2px solid #ccc;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            background-color: #f9f9f9;
        }
        .form-section {
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #ddd;
        }
        .form-section h3 {
            margin-bottom: 10px;
        }
    </style>
"""

st.markdown(form_css, unsafe_allow_html=True)

# MongoDB connection
mongo_client = get_mongo_client(os.getenv("MONGO_URI"))

def check_mongo_connection():
    """Check the MongoDB connection status."""
    if mongo_client:
        try:
            # Attempt to get the database to confirm connection
            db = mongo_client.get_database("company_employees")
            collection = db.get_collection("employees_records")
            st.success("Connected to MongoDB successfully!")
            return True
        except Exception as e:
            st.error(f"Failed to connect to MongoDB: {e}")
            return False
    else:
        st.error("MongoDB client is not available.")
        return False


def user_input_form():
    """Streamlit form to collect data from the user."""
    st.header("Employee Information Form")

    # Start the form context
    with st.form(key="employee_form"):
        # Expandable for basic details
        with st.expander("Basic Details", expanded=True):
            employee_id = st.text_input("Employee ID",max_chars=5)
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            gender = st.selectbox("Gender", ["Male", "Female"])
            min_date = datetime(1970, 1, 1)  # Minimum date: January 1, 1970
            max_date = datetime.now() 
            date_of_birth = st.date_input("Date of Birth",min_value=min_date,max_value=max_date)
            email=st.text_input("email")
            phone_number=st.text_input("Enter your phone number (10 digits):", max_chars=10)

        # Expandable for address
        with st.expander("Address", expanded=True):
            street = st.text_input("Street")
            city = st.text_input("City")
            state = st.text_input("State")
            postal_code = st.text_input("Postal Code")
            country = st.text_input("Country")

        # Expandable for job details
        with st.expander("Job Details", expanded=False):
            job_title = st.selectbox("Job Title",job_titles)
            department = st.selectbox("Department", departments)
            office_location = st.selectbox("Office Location", office_locations)
            hire_date=st.date_input("Hire Date")
            salary=st.number_input("Enter salary")
            currency=st.selectbox("Currency", Currency)
            is_remote = st.checkbox("Remote Worker?")

        # Expandable for skills
        with st.expander("Skills", expanded=False):
            skills = st.text_input("Skills (comma separated)").split(",")

        #Benifits
        with st.expander("Benefits", expanded=False):
            health_insurance = st.selectbox("Insurance", ["Gold Plan", "Silver Plan", "Bronze Plan"])
            retirement_plan = "401K"
            options = list(range(15, 20))
            paid_time_off = st.selectbox("Time-off", options)

        # Expandable for performance reviews
        with st.expander("Performance Reviews", expanded=False):
            performance_reviews = []
            for i in range(2):  # Two reviews for simplicity
                review_date = st.date_input(f"Performance Review {i+1} Date")
                rating = st.slider(f"Rating for Review {i+1}", min_value=1, max_value=5, value=4)
                comments = st.text_input(f"Comments for Review {i+1}")
                performance_reviews.append({"review_date": str(review_date), "rating": rating, "comments": comments})

        # Expandable for additional notes
        with st.expander("Additional Notes", expanded=False):
            notes = st.text_input("Additional Notes")

        # Submit button
        submit_button = st.form_submit_button("Submit Employee Details")

        # Validation and submission
        if submit_button:
            # Validation logic
            missing_fields = []
            if not first_name: missing_fields.append("First Name")
            if not last_name: missing_fields.append("Last Name")
            if not gender: missing_fields.append("Gender")
            if not date_of_birth: missing_fields.append("Date of Birth")
            if not job_title: missing_fields.append("Job Title")
            if not department: missing_fields.append("Department")
            if not office_location: missing_fields.append("Office Location")
            if not skills or all(not skill.strip() for skill in skills): missing_fields.append("Skills")
            if any(not review['review_date'] or not review['rating'] for review in performance_reviews):
                missing_fields.append("Performance Reviews")

            if missing_fields:
                st.error(f"The following fields are required: {', '.join(missing_fields)}")
            else:
                # Prepare data for submission
                employee_data = {
                    "employee_id": employee_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "gender": gender,
                    "date_of_birth": str(date_of_birth),
                    "address": {
                        "street": street,
                        "city": city,
                        "state": state,
                        "postal_code": postal_code,
                        "country": country
                    },
                    "contact_details": {
                        "email": email,
                        "phone_number": phone_number
                    },
                    "job_details": {
                        "job_title": job_title,
                        "department": department,
                        "hire_date": str(hire_date),
                        "employment_type": "Full-time",
                        "salary": salary,
                        "currency": currency
                    },
                    "benefits": {
                        "health_insurance": health_insurance,
                        "retirement_plan": retirement_plan,
                        "paid_time_off": paid_time_off
                    },
                    "skills": skills,
                    "work_location": {
                        "nearest_office": office_location,
                        "is_remote": is_remote
                    },
                    "performance_reviews": performance_reviews,
                    "notes": notes
                }
                # Generate employee string
                employee_string = create_employee_string(employee_data)

                # Generate embedding
                embedding = get_embedding(employee_string)

                   # Check if embedding is empty
                if not embedding:
                    st.error("Embedding has not been generated. Data ingestion was not performed.")
                else:
                    # Add the string and embedding to the data
                    employee_data['employee_string'] = employee_string
                    employee_data['embedding'] = embedding

                    # Push the data to MongoDB
                    if mongo_client:
                        push_data_to_mongo(mongo_client, [employee_data])
                    
                    st.success("Employee data submitted and saved successfully!")


def display_existing_data():
    """Display existing data from MongoDB in the Streamlit app with pagination."""
    if mongo_client:
        db = mongo_client.get_database("company_employees")
        collection = db.get_collection("employees_records")

        # Fetch all employee records
        employees = list(collection.find())
        total_employees = len(employees)
        employees_per_page = 5

        # Initialize session state for page number
        if "page_number" not in st.session_state:
            st.session_state.page_number = 0

        # Calculate start and end indices for the current page
        start_index = st.session_state.page_number * employees_per_page
        end_index = start_index + employees_per_page

        # Display the current page of employees
        st.subheader("Existing Employees Records")
        if employees:
            for employee in employees[start_index:end_index]:
                st.write(f"Name: {employee['first_name']} {employee['last_name']}")
                st.write(f"Job Title: {employee['job_details']['job_title']}")
                st.write(f"Department: {employee['job_details']['department']}")
                st.write(f"Skills: {', '.join(employee['skills'])}")
                st.write(f"Performance Reviews: {employee['performance_reviews']}")
                st.write(f"Location: {employee['work_location']['nearest_office']}, Remote: {employee['work_location']['is_remote']}")
                st.write(f"Notes: {employee['notes']}")
                st.write("---")

            # Display navigation buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("Previous", disabled=start_index == 0):
                    st.session_state.page_number = max(st.session_state.page_number - 1, 0)
            with col3:
                if st.button("Next", disabled=end_index >= total_employees):
                    st.session_state.page_number = min(st.session_state.page_number + 1, total_employees // employees_per_page)

            # Display current page info
            st.caption(f"Showing {start_index + 1} to {min(end_index, total_employees)} of {total_employees} employees.")
        else:
            st.info("No employee records found.")

def main():
    st.title("HR Employee Management System")
    
    # Check MongoDB connection status
    connection_status = check_mongo_connection()

    if connection_status:
        # Option to enter new data or view existing records
        option = st.radio("Choose an action", ("Enter New Employee", "View Existing Employees"))
        
        if option == "Enter New Employee":
            user_input_form()
        elif option == "View Existing Employees":
            display_existing_data()
    else:
        st.warning("Unable to interact with the database. Please check the connection.")

if __name__ == "__main__":
    main()