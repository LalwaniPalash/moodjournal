from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .models import db, User, MoodEntry

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('routes.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    mood_entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.date.desc()).all()
    grouped_entries = {}
    for entry in mood_entries:
        date_str = entry.date.strftime('%Y-%m-%d')
        if date_str not in grouped_entries:
            grouped_entries[date_str] = []
        grouped_entries[date_str].append(entry)
        # No need to sort if there's no specific attribute for sorting
    
    return render_template('dashboard.html', mood_entries=mood_entries, grouped_entries=grouped_entries)

@bp.route('/mood_entry', methods=['GET', 'POST'])
@login_required
def mood_entry():
    if request.method == 'POST':
        mood = request.form.get('mood')
        date_str = request.form.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        tod = request.form.get('tod')
        energy_level = request.form.get('energy_level')
        sleep_quality = request.form.get('sleep_quality')
        activities = request.form.get('activities')
        tags = request.form.get('tags')
        location = request.form.get('location')
        weather = request.form.get('weather')
        custom_notes = request.form.get('custom_notes')

        if energy_level == "Select Energy Level":
            energy_level = None
        if sleep_quality == "Select Sleep Quality":
            sleep_quality = None

        new_entry = MoodEntry(
            user_id=current_user.id,
            mood=mood,
            date=date,
            tod=tod,
            energy_level=energy_level,
            sleep_quality=sleep_quality,
            activities=activities,
            tags=tags,
            location=location,
            weather=weather,
            notes=custom_notes,
        )
        db.session.add(new_entry)
        db.session.commit()
        flash('Mood entry added successfully!', 'success')
        return redirect(url_for('routes.dashboard'))

    return render_template('mood_entry.html')

@bp.route('/delete_mood/<int:id>', methods=['POST'])
@login_required
def delete_mood(id):
    entry = MoodEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('You do not have permission to delete this entry.', 'danger')
        return redirect(url_for('routes.dashboard'))
    
    db.session.delete(entry)
    db.session.commit()
    flash('Mood entry deleted successfully!', 'success')
    return redirect(url_for('routes.dashboard'))
