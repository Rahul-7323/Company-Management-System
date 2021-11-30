from flask_security.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired
from .models import Role, Employee, Department, Project, Team, Client
from .database import db

def unique_dept_name(form, field):
    dept_name = field.data.strip()
    check = db.session.query(Department).filter(Department.dept_name == dept_name).scalar()
    if check:
        raise ValidationError(message="Department name should be unique")
    
def unique_team_name(form, field):
    team_name = field.data.strip()
    check = db.session.query(Team).filter(Team.team_name == team_name).scalar()
    if check:
        raise ValidationError(message="Team name should be unique")
    
def unique_project_name(form, field):
    proj_name = field.data.strip()
    check = db.session.query(Project).filter(Project.proj_name == proj_name).scalar()
    if check:
        raise ValidationError(message="Project name should be unique")

def unique_client_name(form, field):
    client_name = field.data.strip()
    check = db.session.query(Client).filter(Client.clt_name == client_name).scalar()
    if check:
        raise ValidationError(message="Client name should be unique")
    
class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', validators=[DataRequired()])
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name')
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=["male", "female"], validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired()])
    dept_id = SelectField('Department', choices=[])
    team_id = SelectField('Team', choices=[])
    role_id = SelectField('Role', choices=[])
    
class DepartmentForm(FlaskForm):
    dept_name = StringField('Department Name', validators=[DataRequired(),unique_dept_name])
    dept_location = StringField('Location', validators=[DataRequired()])
    mgr_emp_id = SelectField('Manager', choices=[], validators=[DataRequired()])
    
class TeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[DataRequired(),unique_team_name])
    team_descr = StringField('Team Description')
    proj_id = SelectField('Project', choices=[], validators=[DataRequired()])
    mgr_emp_id = SelectField('Team Manager', choices=[])
    
class ProjectForm(FlaskForm):
    proj_name = StringField('Project Name', validators=[DataRequired(), unique_project_name])
    proj_descr = StringField('Project Description')
    clt_id = SelectField('Client', choices=[])
    dept_id = SelectField('Department', choices=[])

class ClientForm(FlaskForm):
    clt_name = StringField('Client Name', validators=[DataRequired(), unique_client_name])


# Update Forms
class UpdateProjectForm(FlaskForm):
    proj_name = StringField('Project Name', validators=[DataRequired()])
    proj_descr = StringField('Project Description')
    clt_id = SelectField('Client', choices=[])
    dept_id = SelectField('Department', choices=[])
    
class UpdateDepartmentForm(FlaskForm):
    dept_name = StringField('Department Name', validators=[DataRequired()])
    dept_location = StringField('Location', validators=[DataRequired()])
    mgr_emp_id = SelectField('Manager', choices=[], validators=[DataRequired()])
    
class UpdateEmployeeForm(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name')
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=["male", "female"], validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired()])
    dept_id = SelectField('Department', choices=[])
    team_id = SelectField('Team', choices=[])
    
class UpdateTeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[DataRequired()])
    team_descr = StringField('Team Description')
    proj_id = SelectField('Project', choices=[], validators=[DataRequired()])
    mgr_emp_id = SelectField('Team Manager', choices=[])