# Appointment Booking System

This is an AI-powered appointment booking system that allows users to check availability and book appointments. The system uses a conversational interface and is built using the Swarm AI framework.

## Features

1. Check appointment availability
2. Book appointments
3. Enforce booking policies
4. Maintain conversation memory
5. Save and load calendar data

## Components

### Main Script (main.py)

The main script serves as the entry point for the application. It initializes the necessary components and runs the main loop for user interaction.

Key components:
- Swarm AI client
- Calendar data
- Booking policies
- Availability Checker agent
- Booking Agent
- Conversation Memory

### Agents

1. **Availability Checker Agent**: Responsible for checking appointment availability.
2. **Booking Agent**: Handles the appointment booking process.

### Helper Classes

1. **AppointmentBooker**: Manages the booking logic and updates the calendar.
2. **AvailabilityChecker**: Checks the availability of appointment slots.
3. **CalendarData**: Handles calendar data storage and retrieval.
4. **BookingPolicies**: Enforces booking rules and policies.

## How it Works

1. The system starts by initializing the Swarm AI client, calendar data, and booking policies.
2. Users interact with the system through a command-line interface.
3. The system uses the Availability Checker agent to handle availability inquiries.
4. When a user wants to book an appointment, the system transfers control to the Booking Agent.
5. The Conversation Memory keeps track of recent interactions to maintain context.
6. Users can save the updated calendar data using the 's' command.
7. The system enforces booking policies, such as business hours and maximum appointments per week.

## Usage

1. Run the `main.py` script to start the application.
2. Interact with the AI assistant using natural language.
3. Check availability by asking about specific dates and times.
4. Book appointments by providing the required information.
5. Use the 'quit' command to exit the application.
6. Use the 's' command to save the updated calendar data.

## Configuration

- The system uses a JSON file (`calendar_data.json`) to store appointment data.
- Booking policies are defined in the `BookingPolicies` class.
- The OpenAI API key is stored in the `.env` file for security.

This appointment booking system provides a flexible and intelligent solution for managing appointments, enforcing policies, and interacting with users through a conversational AI interface.
