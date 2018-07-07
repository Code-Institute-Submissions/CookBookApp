from wtforms import Form, StringField, PasswordField, validators

# Validation of fields for user registration
class RegistrationForm(Form):
    first = StringField('first', [validators.DataRequired(), validators.Length(min=3, max=25)])
    last = StringField('last', [validators.DataRequired(), validators.Length(min=3, max=25)])
    username = StringField('username', [validators.DataRequired(), validators.Length(min=3, max=25)])
    password = PasswordField('password', [validators.DataRequired(), validators.Length(min=4, max=25)])