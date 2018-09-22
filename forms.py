from flask_wtf import Form
from wtforms.fields import *
from wtforms.validators import Required, Email

class SignupForm(Form):
    first_name = TextField(u'First Name', validators=[Required()])
    last_name = TextField(u'Last Name', validators=[Required()])
    email = TextField(u'Email Address', validators=[Email()])
    birthday = DateField(u'Your Birthday')
    phone_number = TextField(u'Cell Phone Number', validators=[Required()])
    income = IntegerField(u'Income', validators=[Required()])
    donated_before = BooleanField(u'Have you donated to Goodwill before?', validators=[Required()])

    submit = SubmitField(u'Submit')
