from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import Required, Email

class SignupForm(FlaskForm):
    firstNameInput = TextField(u'First Name', validators=[Required()])
    lastNameInput = TextField(u'Last Name', validators=[Required()])
    emailInput = TextField(u'Email Address', validators=[Email()])
    phoneNumberInput = TextField(u'Cell Phone Number', validators=[Required()])
    incomeInput = IntegerField(u'Income', validators=[Required()])
    occupationInput = TextField(u'Ocupation', validators=[Required()])
    ageInput = IntegerField(u'Age', validators=[Required()])

    submit = SubmitField(u'Submit')

class LoginForm(FlaskForm):
    lastNameInput = TextField(u'Last Name', validators=[Required()])
    phoneNumberInput = TextField(u'Cell Phone Number', validators=[Required()])

    submit = SubmitField(u'Submit')
