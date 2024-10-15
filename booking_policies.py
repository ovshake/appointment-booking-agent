from datetime import datetime, timedelta

class BookingPolicies:
    def __init__(self):
        # List of booking policies
        self.policies = [
            "Appointments can be scheduled between 9 AM and 4 PM on weekdays.",
            "Each appointment slot is 1 hour long.",
            "If a requested time slot is unavailable, the system should suggest the next available slot.",
            "Clients can book a maximum of two appointments per week."
        ]
        # Maximum number of appointments allowed per week
        self.max_appointments_per_week = 2
        # Define business hours
        self.business_hours = {"start": "09:00", "end": "16:00"}

    def is_within_business_hours(self, time):
        # Check if the given time is within business hours
        return self.business_hours["start"] <= time < self.business_hours["end"]

    def is_weekday(self, date):
        # Check if the given date is a weekday (Monday to Friday)
        return date.weekday() < 5

    def is_valid_appointment_time(self, date, time):
        # Check if the appointment time is valid (weekday and within business hours)
        return self.is_weekday(date) and self.is_within_business_hours(time)

    def can_book_appointment(self, client_id, calendar_data, date):
        # Check if the client has already booked 2 appointments this week
        # Calculate the start and end of the week containing the given date
        week_start = date - timedelta(days=date.weekday())
        week_end = week_start + timedelta(days=6)

        appointment_count = 0
        current_date = week_start
        while current_date <= week_end:
            # Get availability for the current date
            availability = calendar_data.get_availability(current_date)
            for slot in availability:
                # Count appointments for this client
                if not slot['available'] and slot.get('client_id') == client_id:
                    appointment_count += 1
            current_date += timedelta(days=1)

        # Return True if the client has not exceeded the maximum appointments per week
        return appointment_count < self.max_appointments_per_week

    def get_policies(self):
        # Return the list of booking policies
        return self.policies