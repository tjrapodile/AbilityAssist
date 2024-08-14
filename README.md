# AbilityAssist
AbilityAssist is a Django-based web application designed to help students navigate various hotspots around the university campus.
By leveraging Google Maps API and Speech Recognition API, the app provides users with a seamless experience to find their way around campus.

Features:
Destination Selection- Users can select their desired destination from a dropdown menu.
Alternatively, users can use voice recognition to choose from the available options in the dropdown.
Navigation Guidance- The app provides real-time navigation guidance to the selected destination.
Language Support- Currently supports English only.
Responsive Design- Built with the latest version of Bootstrap for a modern and responsive user interface.

Technologies Used:
Backend- Django
Models, Views, Templates
Frontend- JavaScript, Bootstrap (latest version)
API calls made with JavaScript
APIs- Google Maps API for navigation and mapping
Speech Recognition API for voice-activated destination selection

Clone the Repository:
git clone https://github.com/tjrapodile/AbilityAssist.git

Go to the required directory:
cd AbilityAssist

Install Dependencies:
python install requirements.txt

Make sure you have pipenv installed. Then, install the required packages:
pipenv install

Set Up the Database
Run the following command to migrate the database:
python manage.py migrate

Add API Keys:
Obtain API keys for Google Maps and Speech Recognition.
Add them to your environment variables or directly in the settings file.

Run the Development Server:
python manage.py runserver

Access the Application:
Open your web browser and go to http://localhost:8000 to start using AbilityAssist.

Usage:
Select Destination-  Choose your destination from the dropdown menu or use voice recognition to select an option.
Start Navigation- The app will guide you to your selected destination using Google Maps.

Contribution:
Contributions are welcome! If you find any bugs or have suggestions for new features, feel free to open an issue or submit a pull request
