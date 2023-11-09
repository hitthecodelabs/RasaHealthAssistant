# RasaHealthAssistant

RasaHealthAssistant is a Django-based medical appointment management platform designed to facilitate interactions between doctors and patients. This system leverages an intelligent chatbot, built with Rasa, to provide a conversational interface through which users can access personalized information such as medical prescriptions, exercise routines, appointment schedules, and more.

## Features

- **Appointment Management:** Patients can request appointments and doctors can manage them through the web interface.
- **Rasa Chatbot:** Real-time interactions to access profile information, prescriptions, and exercise routines.
- **Customized Profiles:** Patient-specific information for doctors, including medical history and upcoming appointments.
- **Infographics and Routines:** Access to graphical materials on prescribed exercise routines and health tips.

## Tools/Technologies

- Django: The high-level web framework for rapid development.
- Rasa: Building intelligent and contextual chatbots.
- PostgreSQL: Robust and reliable database for data management.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them.
```bash
# Example:
pip install django
pip install rasa
```

## Installing
A step-by-step series of examples that tell you how to get a development environment running.

```bash
# Clone this repository
git clone https://github.com/hitthecodelabs/RasaHealthAssistant.git

# Navigate to the project directory
cd RasaHealthAssistant

# Install dependencies
pip install -r requirements.txt

# Perform database migrations
python manage.py migrate

# Run the server locally
python manage.py runserver
```

## Contributing
Contributions to RasaHealthAssistant are welcome! Here's how you can contribute:

Fork the repository on GitHub.
Create a new branch for your proposed feature or fix.
Commit your changes with an informative description.
Push your branch and submit a pull request.
We appreciate your input!

## License
RasaHealthAssistant is open source software licensed under the MIT License. See the LICENSE file for more details.
