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
import os
from config import AppConfig
from flask_security import auth_required, roles_required
from flask_babel import gettext
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename


# ------- Blueprint init -------
admin_pages = Blueprint("admin_pages", __name__, template_folder="../templates", static_folder="../static")


# ------- Functions -------
def ext_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in AppConfig.ALLOWED_EXTENSIONS


# ------- Page routes -------
@admin_pages.route("/")
@auth_required()
@roles_required("admin")
def index():
    return render_template("admin_index.html")


@admin_pages.route("/publish/newspaper", methods=["GET", "POST"])
@auth_required()
@roles_required("publisher", "admin")
def publish_newspaper():
    if request.method == "POST":
        files = request.files
        credits = request.form.get("credits")
        
        for file in files:
            if (not file) or (not ext_allowed(file.filename)):
                flash(gettext("Invalid input! 102132"), "danger")
                return redirect(url_for(".publish_newspaper"))
        
        if (not files) or (not credits):
            flash(gettext("Invalid input!"), "danger")
            return redirect(url_for(".publish_newspaper"))
        
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(AppConfig.UPLOAD_FOLDER, "newspaper/pdf/en_US", filename))
            return redirect(url_for("download_file", name=filename))
        
    else:
        return render_template("admin/publish_newspaper.html")


@admin_pages.route("/publish/blog", methods=["GET", "POST"])
@auth_required()
@roles_required("publisher", "admin")
def publish_blog():
    return render_template("admin/publish_blog.html")


@admin_pages.route("/publish/update", methods=["GET", "POST"])
@auth_required()
@roles_required("publisher", "admin")
def publish_update():
    return render_template("admin/publish_update.html")