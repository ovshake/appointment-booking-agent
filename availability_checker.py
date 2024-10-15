from datetime import datetime

class AvailabilityChecker:
    def __init__(self, calendar_data, booking_policies):
        # Initialize the AvailabilityChecker with calendar data and booking policies
        self.calendar_data = calendar_data
        self.booking_policies = booking_policies

    def check(self, date_str, time_str):
        # Check availability for a given date and time
        try:
            # Convert string inputs to datetime objects
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            # Return an error message if the date or time format is invalid
            return "Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time."

        # Check if the requested time is within business hours and on a weekday
        if not self.booking_policies.is_valid_appointment_time(date, time_str):
            return "The requested time is outside of our business hours or not on a weekday."

        # Get the availability for the requested date
        availability = self.calendar_data.get_availability(date)
        for slot in availability:
            if slot['start'] == time_str:
                if slot['available']:
                    # If the slot is available, return a confirmation message
                    return f"The slot at {time_str} on {date_str} is available."
                else:
                    # If the slot is not available, find the next available slot
                    next_date, next_time = self.calendar_data.get_next_available_slot(date, time_str)
                    if next_date and next_time:
                        # If a next available slot is found, return its information
                        return f"The requested slot is not available. The next available slot is on {next_date} at {next_time}."
                    else:
                        # If no available slots are found in the next week, inform the user
                        return "No available slots found in the next week."

        # If no slot is found at the specified time, return an error message
        return "No slot found at the specified time."