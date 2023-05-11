#  ICS News Website admin content management module.
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
Admin content management module for the ICS News Website.

Notes
-----
This module is not complete.
"""


# ------- Libraries and utils -------
import os
from datetime import datetime
from config import AppConfig
from flask_security import auth_required, roles_required, current_user
from flask_babel import gettext
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from modules.database import BlogPost, LatestPosts, NewspaperPost, SchoolUpdates
from utils.forms import BlogPostForm, SchoolUpdatePostForm
from werkzeug.utils import secure_filename
from init import db


# ------- Blueprint init -------
content = Blueprint("content", __name__, template_folder="../templates", static_folder="../static")


# ------- Functions -------
def ext_allowed(filename):
    return ("." in filename) and (filename.rsplit(".", 1)[1].lower() in AppConfig.ALLOWED_EXTENSIONS)


# ------- Page routes -------
@content.route("/")
@auth_required()
@roles_required("admin")
def index():
    return redirect(url_for(".publish_index"))


@content.route("/publish")
@auth_required()
@roles_required("admin")
def publish_index():
    return render_template("admin_content/publish_index.html")


@content.route("/publish/newspaper", methods=["GET", "POST"])
@auth_required()
@roles_required("publisher", "admin")
def publish_newspaper():
    if request.method == "POST":
        files = []
        
        for lang in AppConfig.SUPPORTED_LANGS:
            files.append(request.files.get(f"file_{lang}"))
        
        credits = request.form.get("credits")
        
        for file in files:
            if (not file) or (not ext_allowed(file.filename)):
                flash(gettext("Invalid input!"), "danger")
                return redirect(url_for(".publish_newspaper"))
        
        if (not files) or (not credits):
            flash(gettext("Invalid input!"), "danger")
            return redirect(url_for(".publish_newspaper"))
        
        date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = secure_filename(f"pub_{date_time}.pdf")
        
        for i, file in enumerate(files):
            file.save(os.path.join(AppConfig.UPLOAD_FOLDER, f"newspaper/pdf/{AppConfig.SUPPORTED_LANGS[i]}", filename))
            
        date = datetime.now().strftime("%d/%m/%Y")
        title = AppConfig.NEWSPAPER_POSTS_TITLE_FORMAT.format(date=date)
        
        newspaper_db = NewspaperPost(title, None, date_time, date, credits)
        latest_posts_db = LatestPosts("newspaper", title, None, url_for("newspaper_pages.index"), date)
        
        db.session.add(newspaper_db)
        db.session.add(latest_posts_db)
        db.session.commit()
        
        flash(gettext("Successfully published newspaper!"), "success")
        return redirect(url_for(".publish_newspaper"))
        
    else:
        return render_template("admin_content/publish_newspaper.html")


@content.route("/publish/blog", methods=["GET", "POST"])
@auth_required()
@roles_required("publisher", "admin")
def publish_blog():
    form = BlogPostForm()
    form.category.choices = AppConfig.BLOG_CATEGORIES.get("news")
    
    if request.method == "POST" and form.validate_on_submit():
        date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        post = BlogPost("news", form.thumb.data, form.title.data, date_time, form.authors.data, form.category.data, form.body.data)
        
        db.session.add(post)
        db.session.commit()
        
        flash(gettext("Successfully published blog!"), "success")
        return redirect(url_for(".publish_blog")) 
        
    else:
        return render_template("admin_content/publish_blog.html", form=form)


@content.route("/publish/update", methods=["GET", "POST"])
@auth_required()
@roles_required("publisher", "admin")
def publish_update():
    form = SchoolUpdatePostForm()
    form.category.choices = AppConfig.SCHOOL_UPDATE_CATEGORIES
    
    if request.method == "POST" and form.validate_on_submit():
        date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        post = SchoolUpdates(form.title.data, date_time, form.body.data, current_user.username, form.category.data)
        
        db.session.add(post)
        db.session.commit()
        
        flash(gettext("Successfully published school update!"), "success")
        return redirect(url_for(".publish_update")) 
        
    else:
        return render_template("admin_content/publish_update.html", form=form)