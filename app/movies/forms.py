from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search_text = StringField("search")