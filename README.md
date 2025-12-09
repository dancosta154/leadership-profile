# Leadership Portfolio - Flask Application

A professional portfolio website for showcasing leadership documents, experience, and working style.

## Features

- **About Me**: Personal background and professional journey
- **How to Work With Dan**: Communication preferences and collaboration style
- **Insights Discovery**: Personality profile and working preferences
- **Documents Showcase**: Upload and organize leadership documents with categories and filtering
- **Admin Panel**: Secure dashboard for managing documents

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd leadership-profile
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables (optional)**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set:
   - `SECRET_KEY`: A random secret key for session security
   - `ADMIN_PASSWORD`: Your admin password (default is "admin123")

## Running the Application

1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **Open your browser and visit**
   ```
   http://localhost:5000
   ```

## Admin Access

1. **Navigate to the admin login page**
   ```
   http://localhost:5000/admin/login
   ```

2. **Default credentials**
   - Password: `admin123`
   
   **⚠️ Important**: Change the default password in production by setting the `ADMIN_PASSWORD` environment variable!

3. **Admin panel features**
   - Upload new documents (PDF, DOC, DOCX, TXT, images)
   - Edit document details (title, description, category)
   - Mark documents as "featured"
   - Delete documents
   - View all uploaded documents

## Project Structure

```
leadership-profile/
├── app.py                  # Main Flask application
├── models.py               # Database models
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── static/
│   ├── css/
│   │   └── style.css      # All styling
│   ├── images/            # Your photos/images
│   └── uploads/           # Uploaded documents
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # About Me page
│   ├── work-with-me.html  # Working style page
│   ├── insights.html      # Insights Discovery page
│   ├── documents.html     # Documents showcase
│   └── admin/
│       ├── login.html     # Admin login
│       └── dashboard.html # Admin dashboard
└── instance/
    └── portfolio.db       # SQLite database (auto-created)
```

## Customization

### Adding Your Photos

1. Save your photo collage images to `static/images/`
2. Update `templates/index.html` to display your images:
   ```html
   <div class="about-image">
       <img src="{{ url_for('static', filename='images/your-photo.jpg') }}" alt="Dan Costa">
   </div>
   ```

### Updating Content

- **About Me**: Edit `templates/index.html`
- **How to Work with Dan**: Edit `templates/work-with-me.html`
- **Insights Discovery**: Edit `templates/insights.html`

### Styling

All CSS is in `static/css/style.css`. The site uses an executive-appropriate color scheme:
- Primary Navy: #1e3a5f
- Primary Blue: #2c5f8d
- Accent Gold: #c9a961

## Document Categories

Suggested categories for organizing your documents:
- Resume
- Leadership Docs
- Career Growth
- Case Studies
- Insights Discovery
- Frameworks
- Other

You can create any categories you want when uploading documents.

## Security Notes

1. **Change the default admin password** before deploying
2. **Set a strong SECRET_KEY** in production
3. **Use HTTPS** when deploying to production
4. **Consider adding additional authentication** for production use

## Deployment

For production deployment, consider:
- Using a production WSGI server (e.g., Gunicorn)
- Setting up a reverse proxy (e.g., Nginx)
- Using a more robust database (e.g., PostgreSQL)
- Enabling HTTPS with SSL certificates
- Setting proper environment variables

## Troubleshooting

### Database Issues
If you encounter database errors, delete the `instance/portfolio.db` file and restart the application. It will be recreated automatically.

### File Upload Issues
Ensure the `static/uploads/` directory exists and has proper write permissions.

### Port Already in Use
If port 5000 is already in use, modify the last line in `app.py`:
```python
app.run(debug=True, port=5001)  # Use a different port
```

## Support

This is a custom application built for personal use. For questions or issues, refer to the Flask documentation:
- Flask: https://flask.palletsprojects.com/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/

## License

Personal use only.

