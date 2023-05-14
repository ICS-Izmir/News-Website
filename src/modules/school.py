#  ICS News Website School module.
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

""" School module for the ICS News Website.

"""


# ------- Libraries and utils -------
from config import AppConfig
from init import db
from flask import Blueprint, render_template
from flask_security import auth_required, roles_accepted
from modules.database import SchoolUpdates


# ------- Blueprint init -------
school_pages = Blueprint("school_pages", __name__, template_folder="../templates", static_folder="../static")


# ------- Page routes -------
@school_pages.route("/school-updates")
@auth_required()
@roles_accepted("student", "teacher")
def school_updates():
    query = db.session.query(SchoolUpdates).limit(AppConfig.SCHOOL_UPDATES_MAX_DISPLAY).all()
    return render_template("updates_index.html", posts=query)