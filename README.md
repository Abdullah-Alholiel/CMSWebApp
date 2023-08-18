
# 🎓 CMSWebApp: Course Management System for Module Registration

## 📌 Introduction
**CMSWebApp** is a robust Django-based web application designed for students to seamlessly register for modules associated with their courses. As a cornerstone of the Cloud-Based Project module, it integrates monolithic architecture, modern web development practices, and Azure cloud services.
## 🚀 Application Overview

### 📚 Models and Their Functionality:

#### 🔐 Admin Models:
- **Groups**: Django's default model for user groups.
- **Users**: Django's default model for user authentication.
- **Students**: Represents the student users.
- **Courses**: Associates a student with a specific student group.
- **Modules**: Denotes academic modules available for registration. A module can be linked with multiple student groups.
- **Registrations**: Logs the registration of a student to a specific module.
- **Student groups**: A custom model that replaces Django's `Group`. It supports additional attributes like descriptions.

### 🌟 Key Features:

#### For Students:
- 📝 View and update their profile.
- 🔍 Browse and search available modules.
- ✅ Register or unregister from modules within their enrolled course(group).
-  ▶️ Students can search for any book needed, and see reccomended books for modules.
- 📋 View registered modules and registered students.

#### For Admins:
- 🛠 Manage modules (add, edit, delete).
- 🤝 Associate modules with student groups.
- 📚 Manage student groups.
- 👥 View student profiles and registrations.
- 🚫 Control module registration availability and if active.

### 🏗 Architecture:
- Monolithic architecture powered by Django.
- Adheres to the MVC design pattern.
- Utilizes a relational data model.
- Leverages Django ORM for object-relational mapping.
- Incorporates Django REST Framework for API endpoints.

### 🛠 Tech Stack:
- Python
- Django
- Django REST Framework
- Azure MySQL
- Azure App Service
- Azure Blob Storage
- Azure Functions

## 🛠 Installation & Setup:
1. 📦 Clone the repository.
2. 🧰 Install the required dependencies.
3. 🗄 Set up the Azure MySQL Database.
4. ☁ Configure Azure Blob Storage for media and static files.
5. 🚀 Deploy the application on Azure App Service.

## 🔐 Environment Variables:
To ensure the application runs smoothly, configure the necessary environment variables, including Azure connection keys and URLs.

Deployed website ---> cmswebapp-c2091021@azurewebsites.net


# Resource Group Url's
Reseource Group: dtl-22-55-708564-af-c2091021-573928
Deployed Azure App service: cmswebapp-c2091021.azurewebsites.net
Azure Database for MySQL flexible server: cmswebapp-db-group2.mysql.database.azure.com





## 📢 Important Notes for Tutors:
- 📂 **GitHub Repository Access**: All tutors are collaborators on the GitHub repository, granting full access to branches and commit history.
- ☁ **Azure App Service URLs**: The application resides on Azure App Service. Both GUI and REST API URLs are available in the submission text.
- 🔑 **Django Super User Credentials & Environment Variables**: The `README.md` file contains the Django super user's username, password, and vital environment variables. Please refer to these for a comprehensive evaluation.
- 🫡 https://github.com/Abdullah-Alholiel/CMSWebApp
