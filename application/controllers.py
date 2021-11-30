from flask import request, render_template, redirect, url_for
from flask import current_app as app
from flask_security import login_required, roles_required, current_user
from flask_security.utils import hash_password
from .models import User, Role, Employee, Department, Project, Team, Client, RolesUsers
from .forms import (
    ExtendedRegisterForm,
    DepartmentForm,
    TeamForm,
    ProjectForm,
    ClientForm,
    UpdateProjectForm,
    UpdateDepartmentForm,
    UpdateEmployeeForm,
    UpdateTeamForm
) 

 
from .database import db
from main import user_datastore



# Form list functions
def department_list():
    depts = [(dept.dept_id,dept.dept_name) for dept in db.session.query(Department).all()]
    depts = [(None,'None')] + depts
    return depts

def team_list():
    teams = [(team.team_id,team.team_name) for team in db.session.query(Team).all()]
    teams = [(None,'None')] + teams
    return teams

def role_list():
    roles = [(role.id,role.name) for role in db.session.query(Role).all()]
    roles = [(None,'None')] + roles
    return roles

def emp_list():
    emps = [(emp.emp_id,f'emp_id:{emp.emp_id}, f_name:{emp.f_name}') for emp in db.session.query(Employee).all()]
    emps = [(None,'None')] + emps
    return emps

def proj_list():
    projs = [(proj.proj_id,proj.proj_name) for proj in db.session.query(Project).all()]
    projs = [(None,'None')] + projs
    return projs

def client_list():
    clts = [(clt.clt_id,clt.clt_name) for clt in db.session.query(Client).all()]
    clts = [(None,'None')] + clts
    return clts


# Helper Functions
def get_user(user_id):
    user = User.query.filter(User.id == user_id).scalar()
    return user


@app.route("/")
def index():
    return redirect(url_for('home'))


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

#################################### Add ####################################
@app.route("/register", methods = ["GET", "POST"])
@roles_required('admin')
def register():
    form = ExtendedRegisterForm()
    form.dept_id.choices = department_list()
    form.team_id.choices = team_list()
    form.role_id.choices = role_list()
    
    if request.method == "GET":
        return render_template("security/register_user.html",register_user_form = form)
    elif request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = hash_password(form.password.data)
            email = form.email.data
            f_name = form.f_name.data
            l_name = form.l_name.data
            dob = form.dob.data
            gender = form.gender.data
            address = form.address.data
            salary = form.salary.data
            dept_id = form.dept_id.data
            team_id = form.team_id.data
            role_id = form.role_id.data

            # Create the user
            user_datastore.create_user(
                username = username,
                email = email,
                password = password
            )
            db.session.commit()
            
            # get the user object from email
            user = User.query.filter(User.email == email).one()
            
            # Add the role of the user
            if role_id is not None:
                roles_users = RolesUsers(
                    user_id = user.id,
                    role_id = role_id
                )
                db.session.add(roles_users)
                db.session.commit()
            
            # add the employee
            if team_id == 'None':
                team_id = None
            if dept_id == 'None':
                dept_id = None            
            
            emp = Employee(
                f_name = f_name,
                l_name = l_name,
                dob = dob,
                gender = gender,
                address = address,
                salary = salary,
                team_id = team_id,
                dept_id = dept_id,
                user_id = user.id
            )
            db.session.add(emp)
            db.session.commit()
            return redirect(url_for('register'))
        else:
            return render_template("security/register_user.html",register_user_form = form)


@app.route("/add_department",methods = ["GET", "POST"])
@roles_required('admin')
def add_department():
    form = DepartmentForm()
    form.mgr_emp_id.choices = emp_list()
    if request.method == "GET":
        return render_template("add_department.html", form = form)
    elif request.method == "POST":
        if form.validate_on_submit():
            dept_name = form.dept_name.data
            dept_location = form.dept_location.data
            mgr_emp_id = form.mgr_emp_id.data
            
            if mgr_emp_id == "None":
                mgr_emp_id = None
            
            dept = Department(
                dept_name = dept_name,
                dept_location = dept_location,
                mgr_emp_id = mgr_emp_id
            )
            db.session.add(dept)
            db.session.commit()
            return redirect(url_for("add_department"))
        else:
            return render_template("add_department.html", form = form)
        
@app.route("/add_team", methods = ["GET", "POST"])
@roles_required('admin')
def add_team():
    form = TeamForm()
    form.mgr_emp_id.choices = emp_list()
    form.proj_id.choices = proj_list()
    if request.method == "GET":
        return render_template("add_team.html", form = form)
    elif request.method == "POST":
        if form.validate_on_submit():
            team_name = form.team_name.data
            team_descr = form.team_descr.data
            proj_id = form.proj_id.data
            mgr_emp_id = form.mgr_emp_id.data
            
            if proj_id == 'None':
                proj_id = None
            
            if mgr_emp_id == 'None':
                mgr_emp_id = None
            
            team = Team(
                team_name = team_name,
                team_descr = team_descr,
                proj_id = proj_id,
                mgr_emp_id = mgr_emp_id                
            )
            
            db.session.add(team)
            db.session.commit()
            
            return redirect(url_for('add_team'))
        else:
            return render_template("add_team.html", form = form)

@app.route("/add_project", methods = ["GET", "POST"])
@roles_required('admin')
def add_project():
    form = ProjectForm()
    form.clt_id.choices = client_list()
    form.dept_id.choices = department_list()
    if request.method == "GET":
        return render_template("add_project.html", form = form)
    elif request.method == "POST":
        if form.validate_on_submit():
            proj_name = form.proj_name.data
            proj_descr = form.proj_descr.data
            clt_id = form.clt_id.data
            dept_id = form.dept_id.data
            
            if clt_id == "None":
                clt_id = None
            
            if dept_id == "None":
                dept_id = None
            
            proj = Project(
                proj_name = proj_name,
                proj_descr = proj_descr,
                clt_id = clt_id,
                dept_id = dept_id
            )
            
            db.session.add(proj)
            db.session.commit()
            
            return redirect(url_for('add_project'))
        else:
            return render_template("add_project.html", form = form)

@app.route("/add_client", methods = ["GET", "POST"])
@roles_required('admin')
def add_client():
    form = ClientForm()
    if request.method == "GET":
        return render_template("add_client.html", form = form)
    elif request.method == "POST":
        if form.validate_on_submit():
            clt_name = form.clt_name.data
            client = Client(
                clt_name = clt_name
            )
            db.session.add(client)
            db.session.commit()
            return redirect(url_for("add_client"))
        else:
            return render_template("add_client.html", form = form)
################################################################################


#################################### View ####################################
@app.route("/employees")
@roles_required('admin')
def employees():
    emps = Employee.query.all()
    return render_template('employees.html',emps = emps)

@app.route("/departments")
@roles_required('admin')
def departments():
    depts = Department.query.all()
    return render_template('departments.html',depts = depts)

@app.route("/teams")
@roles_required('admin')
def teams():
    teams = Team.query.all()
    return render_template('teams.html',teams = teams)

@app.route("/projects")
@roles_required('admin')
def projects():
    projs = Project.query.all()
    return render_template("projects.html", projs = projs)

@app.route("/clients")
@roles_required('admin')
def clients():
    clts = Client.query.all()
    return render_template("clients.html", clts = clts)

@app.route("/departments/<int:dept_id>/employees")
@roles_required('admin')
def department_employees(dept_id):
    dept = Department.query.filter(Department.dept_id == dept_id).one()
    emps = dept.emps
    return render_template("employees.html", emps = emps)

@app.route("/departments/<int:dept_id>/projects")
@roles_required('admin')
def department_projects(dept_id):
    dept = Department.query.filter(Department.dept_id == dept_id).one()
    projs = dept.projs
    return render_template("projects.html", projs = projs)

@app.route("/teams/<int:team_id>/employees")
@roles_required('admin')
def team_employees(team_id):
    team = Team.query.filter(Team.team_id == team_id).one()
    emps = team.emps
    return render_template("employees.html", emps = emps)
################################################################################


#################################### Delete ####################################
@app.route("/delete_user",methods = ["GET"])
@login_required
def delete_user():
    user_id = current_user.id
    user = get_user(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/employee/<int:emp_id>/delete")
@roles_required('admin')
def delete_employee(emp_id):
    emp = Employee.query.filter(Employee.emp_id == emp_id).one()
    user = emp.user
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('employees'))

@app.route("/department/<int:dept_id>/delete")
@roles_required('admin')
def delete_department(dept_id):
    dept = Department.query.filter(Department.dept_id == dept_id).one()
    db.session.delete(dept)
    db.session.commit()
    return redirect(url_for("departments"))

@app.route("/team/<int:team_id>/delete")
@roles_required('admin')
def delete_team(team_id):
    team = Team.query.filter(Team.team_id == team_id).one()
    db.session.delete(team)
    db.session.commit()
    return redirect(url_for("teams"))

@app.route("/project/<int:proj_id>/delete")
@roles_required('admin')
def delete_project(proj_id):
    proj = Project.query.filter(Project.proj_id == proj_id).one()
    db.session.delete(proj)
    db.session.commit()
    return redirect(url_for("projects"))

@app.route("/client/<int:clt_id>/delete")
@roles_required('admin')
def delete_client(clt_id):
    clt = Client.query.filter(Client.clt_id == clt_id).one()
    db.session.delete(clt)
    db.session.commit()
    return redirect(url_for('clients'))
################################################################################


#################################### Update ####################################
@app.route("/project/<int:proj_id>/update", methods = ["GET", "POST"])
@roles_required('admin')
def update_project(proj_id):
    proj = Project.query.filter(Project.proj_id == proj_id).one()
    form = UpdateProjectForm(obj=proj)
    form.clt_id.choices = client_list()
    form.dept_id.choices = department_list()
    if request.method == "GET":
        return render_template("update_project.html", form = form, proj_id = proj_id)
    elif request.method == "POST":
        if form.validate_on_submit():
            proj.proj_descr = form.proj_descr.data
            proj.clt_id = form.clt_id.data
            proj.dept_id = form.dept_id.data
            proj.proj_name = form.proj_name.data
            db.session.commit()
            return redirect(url_for("projects"))
        else:
            return render_template("update_project.html", form = form, proj_id = proj_id)
        
@app.route("/department/<int:dept_id>/update", methods = ["GET", "POST"])
@roles_required('admin')
def update_department(dept_id):
    dept = Department.query.filter(Department.dept_id == dept_id).one()
    form = UpdateDepartmentForm(obj=dept)
    form.mgr_emp_id.choices = emp_list()
    if request.method == "GET":
        return render_template("update_department.html", form = form, dept_id = dept_id)
    elif request.method == "POST":
        if form.validate_on_submit():
            dept.dept_name = form.dept_name.data
            dept.dept_location = form.dept_location.data
            dept.mgr_emp_id = form.mgr_emp_id.data
            db.session.commit()
            return redirect(url_for("departments"))
        else:
            return render_template("update_department.html", form = form, dept_id = dept_id)

@app.route("/employee/<int:emp_id>/update", methods = ["GET", "POST"])
@roles_required('admin')
def update_employee(emp_id):
    emp = Employee.query.filter(Employee.emp_id == emp_id).one()
    form = UpdateEmployeeForm(obj=emp)
    form.dept_id.choices = department_list()
    form.team_id.choices = team_list()
    if request.method == "GET":
        return render_template("update_employee.html", form = form, emp_id = emp_id)
    elif request.method == "POST":
        if form.validate_on_submit():
            emp.f_name = form.f_name.data
            emp.l_name = form.l_name.data
            emp.dob = form.dob.data
            emp.gender = form.gender.data
            emp.address = form.address.data
            emp.salary = form.salary.data
            emp.team_id = form.team_id.data
            emp.dept_id = form.dept_id.data
            db.session.commit()
            return redirect(url_for("employees"))
        else:
            return render_template("update_employee.html", form = form, emp_id = emp_id)
        
@app.route("/team/<int:team_id>/update", methods = ["GET", "POST"])
@roles_required('admin')
def update_team(team_id):
    team = Team.query.filter(Team.team_id == team_id).one()
    form = UpdateTeamForm(obj=team)
    form.mgr_emp_id.choices = emp_list()
    form.proj_id.choices = proj_list()
    if request.method == "GET":
        return render_template("update_team.html", form = form, team_id = team_id)
    elif request.method == "POST":
        if form.validate_on_submit():
            team.team_name = form.team_name.data
            team.team_descr = form.team_descr.data
            team.proj_id = form.proj_id.data
            team.mgr_emp_id = form.mgr_emp_id.data
            db.session.commit()
            return redirect(url_for("teams"))
        else:
            return render_template("update_team.html", form = form, team_id = team_id)