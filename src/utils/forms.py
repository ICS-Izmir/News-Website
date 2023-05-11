#  ICS News Website WTF forms file.
#  Copyright 2023 Samyar Sadat Akhavi
#  Written by Samyar Sadat Akhavi, 2023.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Forms file for the ICS News Website.

Contains all of the WTForms.
"""


# ------- Libraries and utils -------
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from flask_babel import gettext
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


# ------- WTForms classes -------

# ---- Blog post publication form ----
class BlogPostForm(FlaskForm):
    title = StringField(gettext("Title"), validators=[DataRequired()])
    thumb = StringField(gettext("Thumbnail URL"))
    body = CKEditorField(gettext("Body"), validators=[DataRequired()])
    category = RadioField(gettext("Category"), validators=[DataRequired()], choices=[])
    authors = StringField(gettext("Authors"), validators=[DataRequired()])
    submit = SubmitField(gettext("Submit"))
    
    
# ---- School Update publication form ----
class SchoolUpdatePostForm(FlaskForm):
    title = StringField(gettext("Title"), validators=[DataRequired()])
    body = CKEditorField(gettext("Body"), validators=[DataRequired()])
    category = RadioField(gettext("Category"), validators=[DataRequired()], choices=[])
    submit = SubmitField(gettext("Submit"))