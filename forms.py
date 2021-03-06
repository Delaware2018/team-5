from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import Required, Email

#The SignupForm class is used in __init__.py for the signup web page
#as the inputs here are dictated by certain type fields and whether
#they are required or not

class SignupForm(FlaskForm):
    firstNameInput = TextField(u'First Name', validators=[Required()], render_kw={"placeholder": "First Name"})
    lastNameInput = TextField(u'Last Name', validators=[Required()], render_kw={"placeholder": "Last Name"})
    emailInput = TextField(u'Email', validators=[Email()], render_kw={"placeholder": "Email"})
    phoneNumberInput = TextField(u'Phone Number', validators=[Required()], render_kw={"placeholder": "Phone Number"})
    incomeInput = IntegerField(u'Income', validators=[Required()], render_kw={"placeholder": "Income"})
    occupationInput = TextField(u'Ocupation', validators=[Required()], render_kw={"placeholder": "Occupation"})
    ageInput = IntegerField(u'Age', validators=[Required()], render_kw={"placeholder": "Age"})

    submit = SubmitField(u'Submit')

#The LoginForm class has the same functionality as the SignupForm class however
#it is more limited as a login requires substantially less information than
#is required for Signup

class LoginForm(FlaskForm):
    lastNameInput = TextField(u'Last Name', validators=[Required()], render_kw={"placeholder": "Last Name"})
    phoneNumberInput = TextField(u'Phone Number', validators=[Required()], render_kw={"placeholder": "Phone Number"})

    submit = SubmitField(u'Submit')
