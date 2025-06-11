from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Student
from app.forms import StudentForm, LoginForm  # Importez votre formulaire
#from hashpw import bcrypt

#_________________________Login________________________________________________________
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

#________________________package________________________________________________________
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(student_id):
    return Student.query.get(int(student_id))
#________________________Variable________________________________________________________

@app.route('/<int:student_id>')
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('students/p_student.html', student=student)

#_____________@@@@@@@@@@@@@___________________________________________
@app.route('/signup')
def Home():
    return render_template('signup.html')



#___________Route pour accueil_________________________________________________________________________

@app.route('/Accueil')
def base():
    return render_template('index.html')



#___________Route pour loger d'un etudiant_________________________________________________________________________

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(last_name=form.last_name.data).first()
        if student:
            if bcrypt.check_password_hash(student.mdp, form.mdp.data):
                login_user(student)
                #return redirect(url_for('dashboard'))
                return redirect(url_for('list_students'))
    return render_template('p_login.html', form=form)

#_________________________Login_________________________________________________________


#_________________________La route pour l'Accueil de IHM_________________________________________________________

@app.route('/')
def Accueil():
    return render_template('base.html')


#___________Route pour lister tout les etudiant_________________________________________________________________________

@app.route('/List')
def list_students():
    students = Student.query.all()
    return render_template('students/p_list.html', students=students)

   
#___________Route pour ajouter d'un etudiant_________________________________________________________________________

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.mdp.data)
        #hashed_password = bcrypt.hashpw(form.mdp.data.encode('utf-8'), bcrypt.gensalt())
        student = Student(first_name=form.first_name.data, 
                          last_name=form.last_name.data, 
                          id=form.id.data,
                          phone=form.phone.data,
                          departement=form.departement.data,
                          filiere=form.filiere.data,
                          Level=form.Level.data,
                          academic_year=form.academic_year.data,
                          #mdp=hashed_password, 
                          email=form.email.data)
        db.session.add(student)
        db.session.commit()
        flash("Un studiant a été ajouté avec succées")
        return redirect(url_for('list_students'))
    return render_template('students/p_add.html', title='Ajouter un étudiant', form=form)

#___________Route pour l'editer(Modification) d'un étudiant_________________________________________________________________________

@app.route('/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.phone = form.phone.data
        student.departement = form.departement.data
        student.filiere = form.filiere.data
        student.Level = form.Level.data
        student.academic_year = form.academic_year.data
        student.email = form.email.data
        # ... mettre à jour les autres champs ...
        db.session.commit()
        flash("La modification a été prise en compte")       
        return redirect(url_for('list_students'))
    return render_template('students/p_edit.html', title='Modifier un étudiant', form=form, student=student)

#___________Route pour la Suppréssion d'un etudiant_________________________________________________________________________

@app.route('/<int:student_id>/delete')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
        # ... mettre à jour les autres champs ...
    db.session.delete(student)
    db.session.commit()
    flash("Un studiant a été supprimé avec succées")
    return redirect(url_for('list_students'))
    #return render_template('p_edit.html', title='Modifier un étudiant', form=form, student=student)


#__@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@_____

