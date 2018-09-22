from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import Required, Email

class SignupForm(FlaskForm):
    firstNameInput = TextField(u'First Name', validators=[Required()], render_kw={"placeholder": "First Name"})
    lastNameInput = TextField(u'Last Name', validators=[Required()], render_kw={"placeholder": "Last Name"})
    emailInput = TextField(u'Email', validators=[Email()], render_kw={"placeholder": "Email"})
    phoneNumberInput = TextField(u'Phone Number', validators=[Required()], render_kw={"placeholder": "Phone Number"})
    incomeInput = IntegerField(u'Income', validators=[Required()], render_kw={"placeholder": "Income"})
    occupationInput = TextField(u'Ocupation', validators=[Required()], render_kw={"placeholder": "Ocupation"})
    ageInput = IntegerField(u'Age', validators=[Required()], render_kw={"placeholder": "Age"})

    submit = SubmitField(u'Submit')

class LoginForm(FlaskForm):
    lastNameInput = TextField(u'Last Name', validators=[Required()])
    phoneNumberInput = TextField(u'Phone Number', validators=[Required()], render_kw={"placeholder": "Phone Number"})

    submit = SubmitField(u'Submit')
