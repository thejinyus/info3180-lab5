from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField,TextAreaField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    firstname = StringField('Username', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])
    gender = SelectField('gender', choices=[("m","male"),("f","female")] ,validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])
    location = StringField('location', validators=[InputRequired()])
    biography = TextAreaField('biography', validators=[InputRequired()])
    
    
