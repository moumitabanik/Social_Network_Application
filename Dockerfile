# Use an official Python image as the base image
FROM python:3.10

# Set the working directory to /app
WORKDIR /

# Copy the application code
COPY . .

# Upgrade PIP
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install -r requirements.txt

#Migrate Django project
#RUN python manage.py migrate

# Expose the port
EXPOSE 8000

# Run the command to start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]