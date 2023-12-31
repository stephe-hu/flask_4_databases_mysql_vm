import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from faker import Faker
import random

# Load environment variables
load_dotenv()

# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

# Connection string
conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    f"?charset={DB_CHARSET}"
)

# Create a database engine
db_engine = create_engine(conn_string, echo=False)
fake = Faker()

sample_medications = ['Amoxicillin', 'Ibuprofen', 'Acetaminophen', 'Citalopram', 
                      'Metformin', 'Amlodipine', 'Simvastatin', 
                      'Albuterol', 'Gabapentin']

def insert_fake_data(engine, num_patients=100, num_medications=20, num_patient_medications=150): # Noqa: E501
    # Start a connection
    with engine.connect() as connection:
        # Insert fake data into patients
        for _ in range(num_patients):
            first_name = fake.first_name()
            last_name = fake.last_name()
            date_of_birth = fake.date_of_birth(minimum_age=10, maximum_age=90)
            query = text("INSERT INTO patients (first_name, last_name, date_of_birth) VALUES ""(:first_name, :last_name, :date_of_birth)")
            connection.execute(query, {"first_name": first_name, "last_name": last_name, "date_of_birth": date_of_birth})

        # Insert sample medications into medications
        for medication in sample_medications:
            query = text("INSERT INTO medications (medication_name) VALUES (:medication_name)")
            connection.execute(query, {"medication_name": medication})
        
        # Fetch all patient IDs and medication IDs
        query = text("SELECT patient_id FROM patients")
        patient_ids = [row[0] for row in connection.execute(query).fetchall()]
        query2 = text("SELECT medication_id FROM medications")
        medication_ids = [row[0] for row in connection.execute(query2).fetchall()]
        
        # Insert fake data into patient_medications
        for _ in range(num_patient_medications):
            patient_id = random.choice(patient_ids)
            medication_id = random.choice(medication_ids)
            prescribed_date = fake.date_between(start_date="-5y", end_date="today")
            query = text("INSERT INTO patient_medications (patient_id, medication_id, prescribed_date) VALUES (:patient_id, :medication_id, :prescribed_date)")
            connection.execute(query, {"patient_id": patient_id, "medication_id": medication_id, "prescribed_date": prescribed_date})
        connection.commit() 
if __name__ == "__main__":
    insert_fake_data(db_engine)
    print("Fake data insertion complete!")