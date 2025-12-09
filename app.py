from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from config import Config
from models import db, Document

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Create upload folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def require_admin():
    """Check if user is logged in as admin"""
    return session.get('admin_logged_in', False)

# ============ PUBLIC ROUTES ============

@app.route('/')
def index():
    """Home page with About Me section"""
    return render_template('index.html')

@app.route('/work-with-me')
def work_with_me():
    """How to work with Dan page"""
    return render_template('work-with-me.html')

@app.route('/insights')
def insights():
    """Insights Discovery page"""
    return render_template('insights.html')

@app.route('/documents')
def documents():
    """Documents showcase page"""
    category_filter = request.args.get('category', 'all')
    
    if category_filter == 'all':
        docs = Document.query.order_by(Document.is_featured.desc(), Document.order_index.desc(), Document.upload_date.desc()).all()
    else:
        docs = Document.query.filter_by(category=category_filter).order_by(Document.is_featured.desc(), Document.order_index.desc(), Document.upload_date.desc()).all()
    
    # Get all unique categories for filter
    categories = db.session.query(Document.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('documents.html', documents=docs, categories=categories, current_category=category_filter)

@app.route('/view/<int:doc_id>')
def view_document(doc_id):
    """View a document in browser"""
    doc = Document.query.get_or_404(doc_id)
    return render_template('view_document.html', document=doc)

@app.route('/serve/<int:doc_id>')
def serve_document(doc_id):
    """Serve document file for inline viewing"""
    doc = Document.query.get_or_404(doc_id)
    return send_from_directory(
        os.path.dirname(doc.file_path),
        os.path.basename(doc.file_path),
        as_attachment=False
    )

@app.route('/download/<int:doc_id>')
def download_document(doc_id):
    """Download a document"""
    doc = Document.query.get_or_404(doc_id)
    return send_from_directory(
        os.path.dirname(doc.file_path),
        os.path.basename(doc.file_path),
        as_attachment=True,
        download_name=doc.original_filename
    )

# ============ ADMIN ROUTES ============

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        if check_password_hash(app.config['ADMIN_PASSWORD_HASH'], password):
            session['admin_logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid password', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if not require_admin():
        flash('Please log in to access the admin panel', 'error')
        return redirect(url_for('admin_login'))
    
    docs = Document.query.order_by(Document.upload_date.desc()).all()
    return render_template('admin/dashboard.html', documents=docs)

@app.route('/admin/upload', methods=['POST'])
def admin_upload():
    """Handle document upload"""
    if not require_admin():
        flash('Please log in to access the admin panel', 'error')
        return redirect(url_for('admin_login'))
    
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('admin_dashboard'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Create document record
        doc = Document(
            title=request.form.get('title'),
            description=request.form.get('description'),
            category=request.form.get('category'),
            file_path=filepath,
            original_filename=secure_filename(request.files['file'].filename),
            is_featured=request.form.get('is_featured') == 'on'
        )
        
        db.session.add(doc)
        db.session.commit()
        
        flash(f'Document "{doc.title}" uploaded successfully!', 'success')
    else:
        flash('Invalid file type', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit/<int:doc_id>', methods=['POST'])
def admin_edit(doc_id):
    """Edit document details"""
    if not require_admin():
        flash('Please log in to access the admin panel', 'error')
        return redirect(url_for('admin_login'))
    
    doc = Document.query.get_or_404(doc_id)
    doc.title = request.form.get('title')
    doc.description = request.form.get('description')
    doc.category = request.form.get('category')
    doc.is_featured = request.form.get('is_featured') == 'on'
    
    db.session.commit()
    flash(f'Document "{doc.title}" updated successfully!', 'success')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:doc_id>', methods=['POST'])
def admin_delete(doc_id):
    """Delete a document"""
    if not require_admin():
        flash('Please log in to access the admin panel', 'error')
        return redirect(url_for('admin_login'))
    
    doc = Document.query.get_or_404(doc_id)
    
    # Delete file from filesystem
    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)
    
    # Delete from database
    db.session.delete(doc)
    db.session.commit()
    
    flash(f'Document "{doc.title}" deleted successfully!', 'success')
    
    return redirect(url_for('admin_dashboard'))

# ============ INITIALIZATION ============

def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database initialized!")

if __name__ == '__main__':
    init_db()
    # Get port from environment variable (for production) or use 5001 for development
    port = int(os.environ.get('PORT', 5001))
    # Only enable debug mode in development
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, port=port, host='0.0.0.0')

