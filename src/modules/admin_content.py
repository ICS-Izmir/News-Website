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

""" Admin content management module for the ICS News Website.

"""


# ------- Libraries and utils -------
import os
from datetime import datetime
from config import AppConfig
from flask_security import auth_required, roles_required, current_user
from flask_babel import gettext, get_locale
from flask import Blueprint, flash, redirect, render_template, request, url_for
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
        titles = {}
        thumbnail = request.files.get("thumb")
        credits = request.form.get("credits")
        date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        date = datetime.now().strftime("%d/%m/%Y")
        filename = secure_filename(f"pub_{date_time}")
        
        for lang in AppConfig.SUPPORTED_LANGS:
            if request.files.get(f"file_{lang}") and ext_allowed(request.files.get(f"file_{lang}").filename):
                files.append(request.files.get(f"file_{lang}"))
            
            else:
                flash(gettext("Invalid file input!"), "danger")
                return redirect(url_for(".publish_newspaper"))
            
            if request.form.get(f"title_{lang}"):
                titles.update({lang: request.form.get(f"title_{lang}")})
                
            else:
                flash(gettext("Invalid title input!"), "danger")
                return redirect(url_for(".publish_newspaper"))
        
        for i, file in enumerate(files):
            file.save(os.path.join(AppConfig.NEWSPAPER_DATA_PATH, f"pdf/{AppConfig.SUPPORTED_LANGS[i]}", filename + ".pdf"))
            
        thumbnail.save(os.path.join(AppConfig.NEWSPAPER_DATA_PATH, f"thumbnail/{filename}.{thumbnail.filename.rsplit('.', 1)[1]}"))
        thumbnail_url = f"{AppConfig.NEWSPAPER_DATA_PATH_STATIC_RELATIVE}/thumbnail/{filename}.{thumbnail.filename.rsplit('.', 1)[1]}"
        
        newspaper_db = NewspaperPost(titles, thumbnail_url, date_time, date, credits)
        
        for lang in AppConfig.SUPPORTED_LANGS:
            latest_posts_db = LatestPosts("newspaper", lang, titles.get(lang), thumbnail_url, url_for("newspaper_pages.index"), date)
            db.session.add(latest_posts_db)
        
        db.session.add(newspaper_db)
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
    categories = AppConfig.BLOG_CATEGORIES.get("news")
    form.category.choices = categories.get(str(get_locale()))
    
    if request.method == "POST" and form.validate_on_submit():
        date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        date = datetime.now().strftime("%d/%m/%Y")
        
        for i, cat in enumerate(categories.get(str(get_locale()))):
            if form.category.data == cat:
                category = {}
                
                for lang in AppConfig.SUPPORTED_LANGS:
                    category.update({lang: categories.get(lang)[i]})
                    
                form.category.data = category
        
        post = BlogPost("news", form.lang.data, form.thumb.data, form.title.data, date_time, form.authors.data, form.category.data, form.body.data)
        latest_posts_db = LatestPosts("blog", form.lang.data, form.title.data, form.thumb.data, url_for("index"), date)
        
        db.session.add(post)
        db.session.add(latest_posts_db)
        db.session.commit()
        
        flash(gettext("Successfully published blog!"), "success")
        return redirect(url_for(".publish_blog")) 
        
    return render_template("admin_content/publish_blog.html", form=form)


@content.route("/publish/update", methods=["GET", "POST"])
@auth_required()
@roles_required("publisher", "admin")
def publish_update():
    form = SchoolUpdatePostForm()
    categories = AppConfig.SCHOOL_UPDATE_CATEGORIES
    form.category.choices = categories.get(str(get_locale()))
    
    if request.method == "POST" and form.validate_on_submit():
        date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        for i, cat in enumerate(categories.get(str(get_locale()))):
            if form.category.data == cat:
                category = {}
                
                for lang in AppConfig.SUPPORTED_LANGS:
                    category.update({lang: categories.get(lang)[i]})
                    
                form.category.data = category
        
        post = SchoolUpdates(form.lang.data, form.title.data, date_time, form.body.data, current_user.username, form.category.data)
        
        db.session.add(post)
        db.session.commit()
        
        flash(gettext("Successfully published school update!"), "success")
        return redirect(url_for(".publish_update")) 
        
    return render_template("admin_content/publish_update.html", form=form)