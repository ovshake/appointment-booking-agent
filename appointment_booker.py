from datetime import datetime, timedelta

class AppointmentBooker:
    def __init__(self, calendar_data, booking_policies):
        # Initialize the AppointmentBooker with calendar data and booking policies
        self.calendar_data = calendar_data
        self.booking_policies = booking_policies

    def book(self, date_str, time_str, client_id):
        # Validate client ID
        if not client_id.isalnum():
            return "Invalid client ID. Please use only alphanumeric characters."

        # Parse date and time strings into datetime objects
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return "Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time."

        # Check if the appointment time is valid according to booking policies
        if not self.booking_policies.is_valid_appointment_time(date, time_str):
            return "The requested time is outside of our business hours or not on a weekday."

        # Check if the client has already booked the maximum number of appointments for the week
        if not self.booking_policies.can_book_appointment(client_id, self.calendar_data, date):
            return "You have already booked the maximum number of appointments for this week."

        # Get availability for the requested date
        availability = self.calendar_data.get_availability(date)
        for slot in availability:
            if slot['start'] == time_str:
                if slot['available']:
                    # Book the appointment if the slot is available
                    end_time = (datetime.combine(date, time) + timedelta(hours=1)).strftime("%H:%M")
                    self.calendar_data.update_availability(date, time_str, end_time, False, client_id=client_id)
                    return f"Appointment booked successfully for {date_str} at {time_str}."
                else:
                    # If the slot is not available, find the next available slot
                    next_date, next_time = self.calendar_data.get_next_available_slot(date, time_str)
                    if next_date and next_time:
                        return f"The requested slot is not available. The next available slot is on {next_date} at {next_time}. Would you like to book this instead?"
                    else:
                        return "No available slots found in the next week."

        # If no slot is found at the specified time
        return "No slot found at the specified time."