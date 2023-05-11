#  ICS News Website Newspaper module.
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
Newspaper module for the ICS News Website.

Notes
-----
This module is not complete.
"""


# ------- Libraries and utils -------
import bleach
from init import db
from flask import Blueprint, abort, redirect, render_template, send_from_directory, url_for
from flask_babel import get_locale
from modules.database import NewspaperPost


# ------- Blueprint init -------
newspaper_pages = Blueprint("newspaper_pages", __name__, template_folder="../templates", static_folder="../static")


# ------- Page routes -------
@newspaper_pages.route("/")
def index():
    query = db.session.query(NewspaperPost).limit(8).all()
    query.reverse()
    return render_template("newspaper_index.html", archive_list=query)


@newspaper_pages.route("/view/archive")
def view_archive():
    query = db.session.query(NewspaperPost).all()
    query.reverse()
    return render_template("newspaper/archive.html", archive_list=query)


@newspaper_pages.route("/download/publication/<date_time>")
def download_pub(date_time):
    locale = str(get_locale())
    return send_from_directory("static/user-uploaded/newspaper/pdf/", f"{locale}/pub_{bleach.clean(date_time)}.pdf")


@newspaper_pages.route("/view/publication/<date_time>")
def view_pub(date_time):
    locale = str(get_locale())
    return redirect(url_for("static", filename=f"user-uploaded/newspaper/pdf/{locale}/pub_{bleach.clean(date_time)}.pdf"))