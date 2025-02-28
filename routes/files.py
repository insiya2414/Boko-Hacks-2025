from flask import Blueprint, render_template, request, jsonify, session, send_from_directory, current_app, send_file
from extensions import db
from models.user import User
from models.file import File
import os
import uuid
from werkzeug.utils import secure_filename

# Allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Secure upload folder (stored outside public access)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'secure_uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

files_bp = Blueprint('files', __name__, url_prefix='/apps/files')

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to get current logged-in user
def get_current_user():
    if 'user' not in session:
        return None
    return User.query.filter_by(username=session['user']).first()

# Secure filename generation to prevent overwrites
def generate_secure_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid.uuid4().hex}.{ext}"

@files_bp.route('/')
def files():
    """Render files page with all files uploaded by the current user"""
    print("=== FILES LISTING ROUTE ACCESSED ===")
    
    current_user = get_current_user()
    if not current_user:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    print(f"Loading files for user: {current_user.username} (ID: {current_user.id})")
    
    all_files = File.query.filter_by(user_id=current_user.id).order_by(File.uploaded_at.desc()).all()
    print(f"Found {len(all_files)} files")

    return render_template('files.html', files=all_files, current_user_id=current_user.id)

@files_bp.route('/upload', methods=['POST'])
def upload_file():
    """Secure File Upload with Strict Type Validation"""
    
    current_user = get_current_user()
    if not current_user:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    file = request.files.get('file')
    if not file:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400

    # Secure the filename and prevent overwriting
    filename = secure_filename(file.filename)
    if not allowed_file(filename):
        return jsonify({'success': False, 'error': 'Invalid file type! Allowed: pdf, png, jpg, jpeg, gif'}), 400

    # Generate unique filename
    filename = generate_secure_filename(filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # Save file securely
    file.save(file_path)

    # Save to database
    new_file = File(filename=filename, file_path=file_path, user_id=current_user.id)
    db.session.add(new_file)
    db.session.commit()

    return jsonify({'success': True, 'message': 'File uploaded successfully!', 'file': new_file.to_dict()})

@files_bp.route('/delete/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Secure file deletion"""
    print(f"\n=== FILE DELETE ATTEMPT: ID {file_id} ===")

    current_user = get_current_user()
    if not current_user:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    file_path = file.file_path

    # Delete file from filesystem first
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File deleted from filesystem: {file_path}")
    else:
        print(f"Warning: File not found on filesystem: {file_path}")

    # Remove from database
    db.session.delete(file)
    db.session.commit()
    print(f"File record deleted from database")

    return jsonify({'success': True, 'message': 'File deleted successfully'})

@files_bp.route('/download/<int:file_id>')
def download_file(file_id):
    """Secure file download"""
    print(f"\n=== FILE DOWNLOAD ATTEMPT: ID {file_id} ===")

    current_user = get_current_user()
    if not current_user:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    # Extract directory and filename
    directory = os.path.dirname(file.file_path)
    filename = os.path.basename(file.file_path)

    if os.path.exists(file.file_path):
        print(f"Sending file: {file.file_path}")
        return send_from_directory(directory, filename, as_attachment=True)
    
    print(f"Error: File not found on filesystem: {file.file_path}")
    return jsonify({'success': False, 'error': 'File not found on server'}), 404

@files_bp.route('/stream/<int:file_id>')
def stream_file(file_id):
    """Stream large files instead of loading them into memory"""
    print(f"\n=== FILE STREAM ATTEMPT: ID {file_id} ===")

    current_user = get_current_user()
    if not current_user:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    if os.path.exists(file.file_path):
        return send_file(file.file_path, as_attachment=True)
    
    return jsonify({'success': False, 'error': 'File not found'}), 404
