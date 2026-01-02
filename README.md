# 🎯 Django Blog

A modern, feature-rich blog application built with Django that allows users to create, read, update, and delete blog posts with user authentication and admin panel.

## 🌐 Live Demo
**Live Site:** [https://myblog-b5da.onrender.com](https://myblog-b5da.onrender.com)  
**Admin Panel:** [https://myblog-b5da.onrender.com/admin](https://myblog-b5da.onrender.com/admin)

## ✨ Features

### 🔐 Authentication & Authorization
- User registration and login system
- Password reset functionality
- User profile management
- Secure session handling

### 📝 Blog Management
- Create, read, update, and delete blog posts
- Rich text editor support
- Image upload for posts
- Category and tag system
- Search functionality

### 👥 User Features
- User profiles with avatars
- Comment system on posts
- Like/unlike posts
- Personal dashboard

### 🎨 Modern UI
- Responsive design
- Clean and intuitive interface
- Bootstrap integration
- Mobile-friendly layout

### ⚙️ Admin Features
- Django admin interface
- User management
- Content moderation
- Analytics dashboard

## 🛠️ Technology Stack

### Backend
- **Django 5.2.6** - Python web framework
- **PostgreSQL** - Production database
- **SQLite** - Development database
- **Gunicorn** - WSGI HTTP server
- **WhiteNoise** - Static file serving

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **Bootstrap 5** - CSS framework
- **JavaScript** - Client-side functionality

### Deployment & DevOps
- **Render.com** - Cloud platform
- **Git & GitHub** - Version control
- **Pillow** - Image processing
- **dj-database-url** - Database configuration

## 📦 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (for production)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/PS-gitpro/myblog.git
   cd myblog

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
```bash
pip install -r requirements.txt

4. Environment configuration
```bash
# Create .env file
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3

5. Database setup
```bash
python manage.py migrate
python manage.py createsuperuser

6. Run development server
```bash
python manage.py runserver

Build Command
bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput

📁 Project Structure
text
myblog/
├── myblog/                 # Project settings
│   ├── settings.py         # Configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI config
├── blog/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # Business logic
│   ├── urls.py            # App URLs
│   └── templates/         # HTML templates
├── templates/              # Global templates
├── static/                 # Static files
├── requirements.txt        # Dependencies
└── manage.py              # Django CLI

🔧 Configuration
Environment Variables
DEBUG - Debug mode (True/False)
SECRET_KEY - Django secret key
DATABASE_URL - Database connection string
ALLOWED_HOSTS - Allowed hostnames

Database Configuration
Development: SQLite
Production: PostgreSQL

👨‍💻 Usage
For Users
Register a new account
Login to your account
Create blog posts
Interact with other posts (like, comment)
Manage your profile

For Administrators
Access /admin panel
Manage users and content
Monitor site analytics
Moderate comments and posts

🤝 Contributing
We welcome contributions! Please follow these steps:
Fork the project
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit changes (git commit -m 'Add AmazingFeature')
Push to branch (git push origin feature/AmazingFeature)
Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🐛 Bug Reports & Feature Requests
Found a bug or have a feature request? Please open an issue on GitHub.

🙏 Acknowledgments
Django community for excellent documentation
Render.com for free hosting tier
Bootstrap team for responsive design framework

📞 Support
If you need help with this project:

Check the issues page
Create a new issue with detailed description
Email: contactprateeksingh01@gmail.com

⭐ If you find this project helpful, please give it a star on GitHub!

<div align="center">
🚀 Built with Django & ❤️
https://img.shields.io/badge/Django-5.2.6-green.svg
https://img.shields.io/badge/Python-3.8+-blue.svg
https://img.shields.io/badge/PostgreSQL-Database-blue.svg
https://img.shields.io/badge/Deployed_on-Render.com-blue.svg

</div>
📊 Project Status
https://img.shields.io/badge/build-passing-brightgreen
https://img.shields.io/badge/deployment-live-success
https://img.shields.io/badge/license-MIT-blue
