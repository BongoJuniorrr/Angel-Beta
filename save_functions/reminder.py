import time

class Assistant:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, hour, minute, reminder_message):
        self.reminders.append((hour, minute, reminder_message))

    def check_reminders(self):
        current_time = time.strftime('%H:%M')
        current_hour, current_minute = map(int, current_time.split(':'))

        for hour, minute, reminder_message in self.reminders:
            if current_hour == hour and current_minute == minute:
                print(f"Reminder: {reminder_message}")

    def save_to_log(self, log_filename):
        with open(log_filename, 'w') as file:
            for hour, minute, reminder_message in self.reminders:
                file.write(f"{hour}:{minute} {reminder_message}\n")

    def load_from_log(self, log_filename):
        with open(log_filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(' ')
                time_parts = parts[0].split(':')
                hour, minute = map(int, time_parts)
                reminder_message = ' '.join(parts[1:])
                self.add_reminder(hour, minute, reminder_message)

if __name__ == "__main__":
    assistant = Assistant()

    # Example: Add reminders for 10:30 AM and 3:15 PM
    assistant.add_reminder(10, 30, "Meeting with client")
    assistant.add_reminder(15, 15, "Submit the report")

    # Save reminders to a log file
    assistant.save_to_log("reminders.log")

    # Clear reminders and load them from the log file
    assistant.reminders = []
    assistant.load_from_log("reminders.log")

    while True:
        assistant.check_reminders()
        time.sleep(60)  # Check for reminders every minute
