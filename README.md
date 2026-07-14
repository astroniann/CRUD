# AeroMail - Django Auto-Email Service CRUD Application

AeroMail is a modern, responsive **Auto-Email Campaign Manager** built with Django and Bootstrap 5. It allows users to define email templates, manage campaigns via a comprehensive CRUD interface, and send test emails locally (leveraging Django's console email backend). 

This project demonstrates clean MVC architecture, file attachment management, SQLite database migrations, and responsive front-end design utilizing a custom glassmorphism dark theme.

---

## Key Features

1. **Campaign CRUD Operations**:
   - **Create**: Add new email templates with a subject, rich text body, and optional file attachments (images, documents, PDFs).
   - **Read & Search**: View active campaigns and search by subject query with live table/grid filters.
   - **Update**: Edit subject lines, body copy, or upload new files to existing campaigns.
   - **Delete**: Safely delete unused or obsolete campaign templates.
2. **Mock Email Sender**:
   - Input a target email address to trigger a test send. 
   - Uses Django's console email backend to print output directly to the server terminal, simulating an email service locally without requiring third-party SMTP API keys.
   - Increments the `sent_count` counter upon successful execution.
3. **Premium Visual Aesthetics**:
   - Custom dark mode palette using CSS variables.
   - Elegant glassmorphism containers.
   - Responsive split-screen dashboard (Form on left, templates table on right).
   - Custom floating notifications for success/error events.

---

## Technical Stack

- **Backend**: Python, Django 6.0.7
- **Database**: SQLite3
- **Frontend**: HTML5, Vanilla CSS3, Bootstrap 5.3.0
- **Typography**: Outfit Google Font

---

## Setup & Running Locally

### 1. Prerequisites
Ensure Python is installed on your machine. You can verify this by running:
```bash
python --version
# or on Windows:
py --version
```

### 2. Install Django
Install Django using pip:
```bash
pip install Django
# or using the Windows launcher:
py -m pip install Django
```

### 3. Initialize Database
Apply migrations to set up your SQLite database:
```bash
python manage.py migrate
# or:
py manage.py migrate
```

### 4. Run the Server
Start the Django development server:
```bash
python manage.py runserver
# or:
py manage.py runserver
```

### 5. Access the Web Application
Open your web browser and navigate to:
```url
http://127.0.0.1:8000
```
To view the admin dashboard, create a superuser (`python manage.py createsuperuser`) and visit `http://127.0.0.1:8000/admin/`.

---

## Author
Developed by **Om Patel** as a software engineering portfolio project.
