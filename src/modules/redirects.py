#  ICS News Website blog module.
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
Redirect module for the ICS News Website.

This module is for social and or other redirects.
"""


# ------- Libraries and utils -------
from flask import Blueprint, redirect, send_from_directory, url_for, request, abort, Request
from flask_babel import get_locale
from flask_security import url_for_security
from config import AppConfig
from init import debug_log, log


# ------- Blueprint init -------
redirects = Blueprint("redirects", __name__, static_folder="../static")


# ---- URL config variable checker ----
def check_url(conf_var: dict, req: Request):
    conf_var = conf_var[str(get_locale())]
    
    if conf_var:
        return redirect(conf_var)
    
    log.error(f"[{req.remote_addr}] Failed to load URL for [{req.url}] redirect with language [{str(get_locale())}]")
    debug_log.debug(f"[{req.remote_addr}] Failed to load URL for [{req.url}] redirect with language [{str(get_locale())}]")
    abort(404)


# ------- Page redirects -------
@redirects.route("/blog")
def blog_redirect():
    return redirect(url_for("blog_pages.index"))


@redirects.route("/login")
def login_redirect():
    return redirect(url_for_security("login"))


@redirects.route("/register")
@redirects.route("/signup")
def register_redirect():
    return redirect(url_for_security("register"))


# ------- Social redirects -------
@redirects.route("/twitter")
def twitter_redirect():
    return check_url(AppConfig.TWITTER_URL, request)    


@redirects.route("/instagram")
def instagram_redirect():
    return check_url(AppConfig.INSTAGRAM_URL, request)


@redirects.route("/dc")
@redirects.route("/discord")
def discord_redirect():
    return check_url(AppConfig.DISCORD_URL, request)


@redirects.route("/yt")
@redirects.route("/youtube")
def youtube_redirect():
    return check_url(AppConfig.YOUTUBE_URL, request)


@redirects.route("/open-source")
@redirects.route("/github")
def github_redirect():
    return check_url(AppConfig.GITHUB_URL, request)


@redirects.route("/mail")
@redirects.route("/email")
def email_redirect():
    return check_url(AppConfig.EMAIL_URL, request)


@redirects.route("/discord-ban-appeal")
def discord_ban_appeal_redirect():
    return check_url(AppConfig.DISCORD_BAN_APPEAL_URL, request)


@redirects.route("/suggestions")
def suggestions_redirect():
    return check_url(AppConfig.SUGGESTIONS_URL, request)