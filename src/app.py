#  ICS News Website main application file.
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


# ------- Libraries, utils, and modules -------
import os
import jinja2
import werkzeug
from flask import abort, redirect, render_template, request, session
from flask_security import auth_required, roles_accepted
from config import AppConfig
from flask_babel import get_locale
from init import app, cache, db, log, debug_log
from modules.newspaper import newspaper_pages
from modules.blog import blog_pages
from modules.account import account_pages
from modules.database import LatestPosts, SchoolUpdates, database
from modules.admin import admin_pages
from modules.redirects import redirects
from modules.api import api
from utils.google_analytics import Analytics


# ------- Global variables -------
SUPPORTED_LANGS = AppConfig.SUPPORTED_LANGS
RENDER_CACHE_TIMEOUT = AppConfig.RENDER_CACHE_TIMEOUT


# ------- Jinja env global objects -------
app.jinja_env.globals["get_locale"] = get_locale
app.jinja_env.globals["SUPPORTED_LANGS"] = SUPPORTED_LANGS
app.jinja_env.globals["ENABLE_ANALYTICS"] = AppConfig.ENABLE_ANALYTICS
app.jinja_env.globals["ANALYTICS_TAG_ID"] = AppConfig.ANALYTICS_TAG_ID
app.jinja_env.globals["RENDER_CACHE_TIMEOUT"] = RENDER_CACHE_TIMEOUT
app.jinja_env.globals["WEBSITE_DISPLAY_NAME"] = AppConfig.WEBSITE_DISPLAY_NAME
app.jinja_env.globals["WEBSITE_FOOTER_LOGO"] = AppConfig.WEBSITE_FOOTER_LOGO
app.jinja_env.globals["WEBSITE_NAV_LOGO"] = AppConfig.WEBSITE_NAV_LOGO


# ------- Blueprint registry -------
app.register_blueprint(blog_pages, subdomain="blog")
app.register_blueprint(newspaper_pages, url_prefix="/newspaper")
app.register_blueprint(admin_pages, subdomain="admin")
app.register_blueprint(account_pages, subdomain="account")
app.register_blueprint(api, subdomain="api")
app.register_blueprint(database)
app.register_blueprint(redirects)


# ------- Locale selector -------
@app.route("/set-lang/<lang>", methods=["POST"])
def set_lang(lang):
    if lang in SUPPORTED_LANGS:
        debug_log.debug(f"[{request.remote_addr}] Changed language to [{lang}]")
        session["lang"] = lang
        return redirect(request.referrer)

    abort(500)


# ------- Error handlers -------
@app.errorhandler(werkzeug.exceptions.NotFound)
@cache.cached(timeout=RENDER_CACHE_TIMEOUT)
def error404(error):
    log.info(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}] that resulted in a [404 Error]")
    return render_template("errors/error_404.html"), 404


@app.errorhandler(werkzeug.exceptions.InternalServerError)
@cache.cached(timeout=RENDER_CACHE_TIMEOUT)
def error500(error):
    log.error(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}] that resulted in a [500 Error]")
    return render_template("errors/error_500.html"), 500


@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
@cache.cached(timeout=RENDER_CACHE_TIMEOUT)
def error405(error):
    log.info(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}] that resulted in a [405 Error]")
    return render_template("errors/error_405.html"), 405


@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@cache.cached(timeout=RENDER_CACHE_TIMEOUT)
def template_error(error):
    log.critical(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}] that resulted in a [500 Template Error]")
    return render_template("errors/error_500.html"), 500


# ------- Before request -------
@app.before_request
def maintenance_mode():
    if os.getenv("ENABLE_MAINTENANCE"):
        abort(503)
    

@app.before_request
def remove_www():
    if "://www." in request.url.lower():
        log.info(f"[{request.remote_addr}] Sent a request with [www.]")

        request_url = request.url.lower()
        return redirect(request_url.replace("www.", ""))


@app.before_request
def log_request():
    log.info(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}]")
    

# ------- Page routes -------
@app.route("/")
def index():
    latest_posts = db.session.query(LatestPosts).all()
    latest_posts.reverse()
    return render_template("index.html", page_views=Analytics.pageviews_this_month(), latest_posts=latest_posts)


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@app.route("/school-updates")
@auth_required()
@roles_accepted("student", "teacher")
def school_updates():
    query = db.session.query(SchoolUpdates).limit(40).all()
    return render_template("updates_index.html", posts=query)


# ------- Running the app -------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run()
