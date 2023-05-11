from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 3:
            flash('Note is too short!',
                  category='error')
        else:
            new_note = Note(note_data=note, user_id=current_user.id)
            print(f'note_data: {note}')
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added!', category='success')
            return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user)


@views.route('/note_bin', methods=['GET', 'POST'])
@login_required
def note_bin():
    return render_template("note_bin.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    deleted_note_data = note.note_data
    if note:
        if note.user_id == current_user.id:
            print(f"note_data deleted : {deleted_note_data}")
            db.session.delete(note)
            db.session.commit()
            flash('Note Deleted!', category='success')

    return jsonify({})


@views.route('/edit', methods=['GET', 'POST'])
@login_required
def editPage():
    note_id = request.form.get('note_id')
    note_to_edit = Note.query.filter_by(id=note_id).first()
    if request.method == 'POST':
        return render_template('edit.html', note=note_to_edit, user=current_user)


@views.route('/editSave', methods=['GET', 'POST'])
@login_required
def editSave():
    note_id = request.form.get('note_id')
    note_to_edit = Note.query.filter_by(id=note_id).first()
    edited_note_data = request.form.get('edited_note')

    if request.method == 'POST':
        if note_to_edit is None:
            flash('Note Not Found', category='error')
            return redirect(url_for('views.home'))
        else:
            if len(edited_note_data) < 3:
                flash('Note is too short!',
                      category='error')
            else:
                print(f'note_id: {note_id}')
                print(f'edited_note_data: {edited_note_data}')
                note_to_edit.note_data = edited_note_data  # Update the note data
                db.session.commit()
                flash('Edit Saved!', category='success')
                return redirect(url_for('views.home'))

    return render_template('edit.html', note=note_to_edit, user=current_user)
