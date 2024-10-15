import json
from datetime import datetime, timedelta

class CalendarData:
    def __init__(self, file_path):
        # Load calendar data from a JSON file
        with open(file_path, 'r') as file:
            self.data = json.load(file)

    def get_availability(self, date):
        # Get availability for a specific date
        date_str = date.strftime("%Y-%m-%d")
        return self.data.get(date_str, [])

    def update_availability(self, date, start_time, end_time, available, client_id):
        # Update or add a new availability slot
        date_str = date.strftime("%Y-%m-%d")
        assert start_time < end_time, "End time must be after start time."

        # Create a new date entry if it doesn't exist
        if date_str not in self.data:
            self.data[date_str] = []

        # Check if the slot already exists
        slot_exists = False
        for slot in self.data[date_str]:
            if slot['start'] == start_time and slot['end'] == end_time:
                slot['available'] = available
                slot['client_id'] = client_id
                slot_exists = True
                break

        # If the slot does not exist, add a new one
        if not slot_exists:
            new_slot = {"start": start_time, "end": end_time, "available": available, "client_id": client_id}
            self.data[date_str].append(new_slot)
            self.data[date_str].sort(key=lambda x: x['start'])

    def save(self, file_path):
        # Save the current calendar data to a JSON file
        with open(file_path, 'w') as file:
            json.dump(self.data, file, indent=2)

    def get_next_available_slot(self, date, start_time):
        # Find the next available slot within a week
        current_date = date
        while current_date < date + timedelta(days=7):  # Look for slots within the next week
            availability = self.get_availability(current_date)
            for slot in availability:
                if slot['available'] and slot['start'] >= start_time:
                    return current_date, slot['start']
            current_date += timedelta(days=1)
            start_time = "09:00"  # Reset to the start of the day
        return None, None