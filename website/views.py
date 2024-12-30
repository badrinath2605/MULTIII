from flask import Blueprint,render_template,request, flash,jsonify,session
from flask_login import login_required, current_user
from . import badridb
from .database import User, Note
# from notepad import Notepad
import subprocess
import os
import sys
UPLOAD_FOLDER='website/static/images'

views=Blueprint('views',__name__)


@views.route('/display_note',methods=["POST"])
@login_required
def display_note():
        try:
            # Use sys.executable to get the path to the Python interpreter
            python_executable = sys.executable
            # Construct the absolute path to the notepad.py script
            script_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'notepad.py')

            # For debugging purposes: print the paths to ensure they are correct
            print(f"Executing script with: {python_executable} {script_path}")
            current_user_info=str(current_user.id)
            # Use subprocess to open the Tkinter window
            subprocess.Popen([python_executable, script_path, current_user_info])
            return jsonify({"status": "success"}), 200
        except Exception as e:
            print(f"Error occurred: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500


@views.route('/create_folder', methods=['POST'])
@login_required
def new_folder():
    data = request.get_json()
    folder_name = data.get('folderName')
    if folder_name:
        # Here you can add your logic to save the folder name to the database
        newfol=Note(user_id=current_user.id,floder=folder_name)
        badridb.session.add(newfol)
        badridb.session.commit()
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Folder name is required"}), 400


@views.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method=="POST":
        photo=request.files["profilePhoto"]
        data=request.form
        if photo:
            photo.save(os.path.join(UPLOAD_FOLDER, photo.filename))
            current_user.profile_photo="../static/images/"+photo.filename
        for i in data:
            if i or i=='dob':
                current_user.dob=data[i]
            elif i or i=='yearOfStudy':
                current_user.yearOfStudy = data[i]
            elif i or i=='mobile':
                current_user.mobilenumber=data[i]
            else:
                pass
        badridb.session.commit()
    return render_template('profile.html',user=current_user)

@views.route('/login_home',methods=['GET','POST'])
@login_required
def login_home():
    aflofolders=set(note.floder for note in current_user.notes)
    fullpack=notes = Note.query.filter_by(user_id=current_user.id).all()
    print(fullpack)
    folder_files=dict()
    folset=set()
    for pack in fullpack:
        print(folder_files)
        if pack.floder in folder_files:
            print(pack.floder,"hi",pack.file_name,pack.data)
            folder_files[pack.floder].append([pack.file_name,pack.data])
            print(folder_files[pack.floder],"and")
        else:
            folder_files[pack.floder] =[[pack.file_name,pack.data]]
            print(folder_files[pack.floder],"else")
        folset.add(pack.floder)
    # folder_files=[{pack.floder: [pack.file_name,pack.data]} for pack in fullpack]
    print(folder_files,folset)
    # for i in folder_files:
    #         folder
     #call the function to return filename and content
     # if len(note)<1:
     #     flash('note is too short!',category='error')
     # else:
     #     new_note=Note(data=note,user_id=current_user.id)
     #     badridb.session.add(new_note)
     #     badridb.session.commit()
     #     flash('Note added',category='success')

     # data=request.get_json()
     # print("hi")
     # folder_name=data.get('folderName')
     # if folder_name:
     #     print("hi")
     # new_folder=Note(floder='badri', user_id=current_user.id)
     # badridb.session.add(new_folder)
     # badridb.session.commit()
     #     flash('folder added!',category='success')

    return render_template("login_home.html", folset=aflofolders,fulldata=folder_files)
# <!--<form action="{{ url_for('backend_function') }}" method="post">-->
# <!--  <input type="submit" value="Call Backend Function">-->
# <!--</form>-->