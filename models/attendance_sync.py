from odoo import models, fields, api
import requests
from odoo.exceptions import UserError

class AttendanceSync(models.Model):
    _name = 'attendance.sync'
    _description = 'Attendance Sync'

    @api.model
    def fetch_and_add_attendance(self):
        # Replace with your API details
        api_url = "http://essl-device-api-url/punch_logs"
        api_key = "your_api_key"

        try:
            # Fetch data from eSSL API
            response = requests.get(api_url, headers={"Authorization": f"Bearer {api_key}"})
            if response.status_code != 200:
                raise UserError(f"Failed to fetch attendance logs: {response.text}")

            punch_logs = response.json()  # Assuming the API returns JSON data
            for log in punch_logs:
                # Match the employee in Odoo using a unique identifier
                employee = self.env['hr.employee'].search([('external_id', '=', log['employee_id'])], limit=1)
                if not employee:
                    continue  # Skip if employee is not found

                # Check if this log already exists (by employee and timestamp)
                existing_attendance = self.env['hr.attendance'].search([
                    ('employee_id', '=', employee.id),
                    ('check_in', '=', log['check_in'])
                ], limit=1)

                if not existing_attendance:
                    # Create a new attendance record with check-in time
                    attendance = self.env['hr.attendance'].create({
                        'employee_id': employee.id,
                        'check_in': log['check_in'],
                        'check_out': log.get('check_out')  # Add check-out if available
                    })
                else:
                    # Update the existing record with check-out time if not already set
                    if not existing_attendance.check_out and log.get('check_out'):
                        existing_attendance.write({
                            'check_out': log['check_out']
                        })

        except Exception as e:
            raise UserError(f"An error occurred: {str(e)}")
