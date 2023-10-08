from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd
from pandas import read_sql
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

app = Flask(__name__)

load_dotenv()  # Load environment variables from .env file

# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

# Connection string
conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    "?charset=utf8mb4"
)

# Database connection settings
db_engine = create_engine(conn_string, echo=False)

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/patients')
def patients():
    query_patients = "SELECT * FROM patients"
    df_patients = read_sql(query_patients, db_engine)
    data_patients = df_patients.to_dict(orient='records')
    return render_template('patients.html', data=data_patients)

@app.route('/medications')
def medications():
    query_medications = "SELECT * FROM medications"
    df_medications = read_sql( query_medications, db_engine)
    data_medications = df_medications.to_dict(orient='records')
    return render_template('medications.html', data=data_medications)

@app.route('/patient_medications')
def patient_medications():
    query_patient_medications = "SELECT * FROM patient_medications"
    df_patient_medications = read_sql(query_patient_medications, db_engine)
    data_patient_medications = df_patient_medications.to_dict(orient='records')
    return render_template('patient_medications.html', data=data_patient_medications)

if __name__ == '__main__':
    app.run(debug=True)
    
