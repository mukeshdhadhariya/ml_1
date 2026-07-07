from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import numpy as np
import joblib

from database import engine, get_db
from models import Base, Prediction
from schemas import Employee, PredictionResponse

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Employee Attrition Prediction API",
    description="Predict employee attrition using a trained Machine Learning model.",
    version="1.0.0"
)

# Load trained model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")


@app.get("/")
def home():
    return {
        "message": "Employee Attrition Prediction API is running."
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(employee: Employee, db: Session = Depends(get_db)):

    # Convert input into model feature order
    features = np.array([[
        employee.Age,
        employee.BusinessTravel,
        employee.DailyRate,
        employee.Department,
        employee.DistanceFromHome,
        employee.Education,
        employee.EducationField,
        employee.EnvironmentSatisfaction,
        employee.Gender,
        employee.HourlyRate,
        employee.JobInvolvement,
        employee.JobLevel,
        employee.JobRole,
        employee.JobSatisfaction,
        employee.MaritalStatus,
        employee.MonthlyIncome,
        employee.MonthlyRate,
        employee.NumCompaniesWorked,
        employee.OverTime,
        employee.PercentSalaryHike,
        employee.PerformanceRating,
        employee.RelationshipSatisfaction,
        employee.StockOptionLevel,
        employee.TotalWorkingYears,
        employee.TrainingTimesLastYear,
        employee.WorkLifeBalance,
        employee.YearsAtCompany,
        employee.YearsInCurrentRole,
        employee.YearsSinceLastPromotion,
        employee.YearsWithCurrManager
    ]])

    # Scale input
    features = scaler.transform(features)

    # Predict
    prediction = model.predict(features)[0]

    result = "Leave" if prediction == 1 else "Stay"

    # Save prediction in database
    prediction_record = Prediction(
        age=employee.Age,
        department=employee.Department,
        job_role=employee.JobRole,
        monthly_income=employee.MonthlyIncome,
        total_working_years=employee.TotalWorkingYears,
        years_at_company=employee.YearsAtCompany,
        overtime=employee.OverTime,
        prediction=result
    )

    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)

    return PredictionResponse(
        prediction=result
    )