
# Social Networking Application

This project builds a lightweight social network API. Users can sign up with just an email and log in with email/password. It offers search by email or name (partial match), friend request sending/accepting/rejecting, friend list viewing, and pending friend request listing. To prevent spam, friend request sending has a rate limit.



## Getting Started

To get started with the Social Network Application website, follow these steps:

- Clone the repository to your local machine.
```bash
  git clone https://github.com/moumitabanik/Social_Network_Application.git

```
- Navigate to the Project Directory: Change into the project directory.
```bash
cd Social_Network_Application
```
- Create a Virtual Environment: Create a new virtual environment for the project.
``` bash
python -m venv venv
```
- Activate the Virtual Environment: Activate the virtual environment.
On macOS/Linux:
``` bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```
- Dependencies: Install the required dependencies using pip.
```bash
pip install -r requirements.txt
```
- Database Configuration: Create a MySQL database for the application. Update the database configuration in the settings.py file
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
- Replace 'your_database_name', 'your_database_user', and 'your_database_password' with your actual database information.

- Database Configuration: Create a MySQL database for the application. Update the database configuration in the settings.py file
```bash
python manage.py migrate
```
- Run the Development Server: Start the Django development server.
```bash
python manage.py runserver
```
- Access the Application: Open your web browser and navigate to http://localhost:8000 to access the Health Symptom Recommendation System.
## Tech Stack

Python, Django, REST APIs, MySQL


## API Documentation

Here is the [API Documentation](https://documenter.getpostman.com/view/35389895/2sA3Qy79rk) of the project 


## Appendix

- [Django Documentation](https://docs.djangoproject.com/en/5.0/): Official documentation for the Django web framework.
- [REST Framework Documentation](https://www.django-rest-framework.org/): Documentation for Django REST Framework, which is used for building APIs in Django.
## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/moumita-banik/)

