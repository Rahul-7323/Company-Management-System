from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from .database import db
from flask_security import UserMixin, RoleMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary = 'roles_users')
    employee = db.relationship('Employee', backref = db.backref('user', uselist = False), primaryjoin = "User.id == Employee.user_id", uselist = False, cascade = "all, delete")
    
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False, unique = True)
    description = db.Column(db.String)
    
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    __table_args__ = (
        PrimaryKeyConstraint('user_id','role_id'),
    )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete = "CASCADE"))
    
class Employee(db.Model):
    __tablename__ = 'employee'
    emp_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    f_name = db.Column(db.String, nullable = False)
    l_name = db.Column(db.String)
    dob = db.Column(db.String, nullable = False)
    gender = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)
    salary = db.Column(db.Integer)
    team_id = db.Column(db.Integer, db.ForeignKey("team.team_id"))
    dept_id = db.Column(db.Integer, db.ForeignKey("department.dept_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    # dept, user, team


class Department(db.Model):
    __tablename__ = 'department'
    dept_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    dept_name = db.Column(db.String, nullable = False, unique = True)
    dept_location = db.Column(db.String, nullable = False)
    mgr_emp_id = db.Column(db.Integer, db.ForeignKey("employee.emp_id"))
    mgr_emp = db.relationship('Employee', uselist = False, primaryjoin = "Department.mgr_emp_id == Employee.emp_id")
    emps = db.relationship('Employee', backref = db.backref('dept', uselist = False), primaryjoin = "Department.dept_id == Employee.dept_id")
    projs = db.relationship('Project', backref = db.backref('dept', uselist = False), primaryjoin = "Department.dept_id == Project.dept_id")

    
class Project(db.Model):
    __tablename__ = 'project'
    proj_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    proj_name = db.Column(db.String, nullable = False, unique = True)
    proj_descr = db.Column(db.String)
    clt_id = db.Column(db.Integer, db.ForeignKey("client.clt_id"))
    dept_id = db.Column(db.Integer, db.ForeignKey("department.dept_id"))
    clt = db.relationship('Client', backref = db.backref('proj', uselist = False), foreign_keys = [clt_id], uselist = False)
    # dept
    
class Team(db.Model):
    __tablename__ = 'team'
    team_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    team_name = db.Column(db.String, nullable = False, unique = True)
    team_descr = db.Column(db.String)
    proj_id = db.Column(db.Integer, db.ForeignKey("project.proj_id"))
    mgr_emp_id = db.Column(db.Integer, db.ForeignKey("employee.emp_id"))
    mgr_emp = db.relationship('Employee', uselist = False, primaryjoin = "Team.mgr_emp_id == Employee.emp_id")
    proj = db.relationship('Project', uselist = False, primaryjoin = "Team.proj_id == Project.proj_id")
    emps = db.relationship('Employee', backref = db.backref('team', uselist = False), primaryjoin = "Team.team_id == Employee.team_id")
    
class Client(db.Model):
    __tablename__ = 'client'
    clt_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    clt_name = db.Column(db.Integer, nullable = False, unique = True)