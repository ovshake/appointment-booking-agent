from swarm import Swarm, Agent
# Import custom tools
from availability_checker import AvailabilityChecker
from appointment_booker import AppointmentBooker
from calendar_data import CalendarData
from booking_policies import BookingPolicies
import os

from dotenv import load_dotenv
load_dotenv()

# Set up OpenAI API key
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
client = Swarm()

# Initialize components
calendar_data = CalendarData("calendar_data.json")
booking_policies = BookingPolicies()

# Function to check appointment availability
def check_availability(date_str, time_str):
    checker = AvailabilityChecker(calendar_data, booking_policies)
    return checker.check(date_str, time_str)

# Function to book an appointment
def book_appointment(date_time_client):
    booker = AppointmentBooker(calendar_data, booking_policies)
    date, time, client_id = date_time_client.split(',')
    return booker.book(date, time, client_id)

# Functions to transfer between agents
def transfer_to_booking_agent():
    return booking_agent

def transfer_to_availability_agent():
    return availability_agent

# Define the Availability Checker Agent
availability_agent = Agent(
    name="Availability Checker",
    instructions="""
    You are an AI assistant responsible for checking appointment availability.
    When asked about availability, use the check_availability function. If the slot is available, provide the confirmation message.
    The check_availability function takes a date (date_str) and time (time_str) argument in the format "%Y-%m-%d" and "%H:%M" in the same order.
    If the user wants to book an appointment, transfer to the Booking Agent.
    """,
    functions=[check_availability, transfer_to_booking_agent],
)

# Define the Booking Agent
booking_agent = Agent(
    name="Booking Agent",
    instructions="""
    You are an AI assistant responsible for booking appointments.
    Use the book_appointment function to book appointments. Make sure client id is always asked. 
    The input should be in the format: 'YYYY-MM-DD,HH:MM,client_id'
    """,
    functions=[book_appointment, transfer_to_availability_agent],
)

# Class to maintain conversation memory
class ConversationMemory:
    def __init__(self, max_turns=5):
        self.messages = []
        self.max_turns = max_turns

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_turns * 2:  # Each turn has a user message and an AI response
            self.messages = self.messages[-self.max_turns * 2:]

    def get_messages(self):
        return self.messages

# Main function to run the appointment booking system
def main():
    memory = ConversationMemory(max_turns=2)
    current_agent = availability_agent

    while True:
        user_input = input("User: ")
        if user_input.lower() == 'quit':
            break

        # Save calendar data if 's' is entered
        if user_input.lower() == 's':
            calendar_data.save('calendar_data_modified.json')
            print("Calendar data saved.")
            continue

        # Add user input to conversation memory
        memory.add_message("user", user_input)

        # Run the current agent with the conversation memory
        response = client.run(
            agent=current_agent,
            messages=memory.get_messages(),
        )

        # Process and display AI response
        ai_response = response.messages[-1]["content"]
        memory.add_message("assistant", ai_response)
        print(f"AI: {ai_response}")

        # Check if we need to switch agents
        if response.agent != current_agent:
            current_agent = response.agent
            print(f"Transferring to {current_agent.name}...")

if __name__ == "__main__":
    main()