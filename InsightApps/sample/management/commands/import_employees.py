# sample/management/commands/import_employees.py

import json
from django.core.management.base import BaseCommand
from sample.models import Employees
from django.db import transaction

class Command(BaseCommand):
    help = 'Import employee data from a JSON file into the Employee table'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, 'r') as file:
            data = json.load(file)
            
            # Prepare a list of Employee instances
            employees = [
                Employees(
                    eeid=item['eeid'],
                    full_name=item['full_name'],
                    job_title=item['job_title'],
                    department=item['department'],
                    business_unit=item['business_unit'],
                    gender=item['gender'],
                    ethnicity=item['ethnicity'],
                    age=item['age'],
                    hire_date=item['hire_date'],
                    annual_salary=item['annual_salary'],
                    bonus_percentage=item['bonus_percentage'],
                    country=item['country'],
                    city=item['city']
                )
                for item in data
            ]

            # Insert records in bulk
            with transaction.atomic():
                Employees.objects.using('example').bulk_create(employees)

        self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {json_file}'))
