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
from flask_security import current_user
from flask import Blueprint, abort, request, url_for
from modules.admin_content import content


# ------- Blueprint init -------
admin_pages = Blueprint("admin_pages", __name__, template_folder="../templates", static_folder="../static")
admin_pages.register_blueprint(content, subdomain="admin", url_prefix="/content")


# ------- Access control -------
@admin_pages.before_request
def authenticate():
    if request.path.startswith("/content/"):
        if current_user.is_authenticated and current_user.has_role("publisher"):
            return  
        
        abort(403)
            
    else:
        if current_user.is_authenticated and current_user.has_role("admin"):
            return  
        
        abort(403)


# ------- Page routes -------
@admin_pages.route("/")
def index():
    return f"Main admin page is under construction. For publishing content, please go to <a href='{url_for('.content.publish_index')}'>the publishing page</a>.", 503