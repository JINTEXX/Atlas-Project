# Import required modules
import os
import django

# Create a new Django project
os.system('django-admin startproject Atlas')

# Change into the new project directory
os.chdir('Atlas')

# Create a new Django app for user management
os.system('python manage.py startapp user_management')
