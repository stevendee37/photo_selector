from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField
from wtforms.validators import DataRequired

class PictureForm(FlaskForm):
    image = MultipleFileField('image', validators=[DataRequired()])
    submit = SubmitField('Submit')