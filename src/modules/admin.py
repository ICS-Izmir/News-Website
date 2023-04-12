#  ICS News Website admin module.
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
Admin module for the ICS News Website.

Notes
-----
This module is not complete.
"""


# ------- Libraries and utils -------
from flask_security import auth_required, roles_required
from flask import Blueprint, render_template


# ------- Blueprint init -------
admin_pages = Blueprint("admin_pages", __name__, template_folder="../templates", static_folder="../static")


# ------- Page routes -------
@admin_pages.route("/")
@auth_required()
@roles_required("publisher", "admin")
def index():
    return render_template("admin_index.html")