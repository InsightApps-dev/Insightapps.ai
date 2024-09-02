# sample/models.py

from django.db import models

class Employees(models.Model):
    eeid = models.CharField(primary_key=True,max_length=10)  # Employee ID
    full_name = models.CharField(max_length=100)  # Full Name
    job_title = models.CharField(max_length=100)  # Job Title
    department = models.CharField(max_length=50)  # Department
    business_unit = models.CharField(max_length=50)  # Business Unit
    gender = models.CharField(max_length=10)  # Gender
    ethnicity = models.CharField(max_length=50)  # Ethnicity
    age = models.PositiveIntegerField()  # Age
    hire_date = models.DateTimeField()  # Hire Date
    annual_salary = models.DecimalField(max_digits=10, decimal_places=2)  # Annual Salary
    bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Bonus Percentage
    country = models.CharField(max_length=50)  # Country
    city = models.CharField(max_length=50)  # City

    class Meta:
        db_table = 'employees'