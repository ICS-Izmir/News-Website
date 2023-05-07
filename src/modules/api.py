#  ICS News Website API module.
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
API module for the ICS News Website.

Notes
-----
This module is not complete.
"""


# ------- Libraries and utils -------
import bleach
from flask import Blueprint, abort, render_template, request, url_for
from init import db
from modules.database import Newspaper


# ------- Blueprint init -------
api = Blueprint("api", __name__, template_folder="../templates", static_folder="../static")


# ------- API models -------

# ---- Newspaper model ----
class NewspaperApi():
    file_datetime: str 
    filename: str
    pdf_view_url: str
    pdf_download_url: str
    publication_num: int
    date: str 
    credits: str

    def __init__(self, file_datetime: str, filename: str, pdf_view_url: str, pdf_download_url: str, publication_num: int, date: str, credits: str):
        self.file_datetime = file_datetime
        self.fliename = filename
        self.pdf_view_url = pdf_view_url
        self.pdf_download_url = pdf_download_url
        self.publication_num = publication_num
        self.date = date
        self.credits = credits


# ------- Page routes -------
@api.route("/")
def index():
    return render_template("api_index.html")


@api.route("/documentation/v1")
def v1_documentation():
    return render_template("api/documentation.html")
              
              
@api.route("/v1/get/newspaper/<filter>")
def v1_get_newspaper(filter):
    query = request.args.get("query")
    
    if filter == "archive":
        query = db.session.query(Newspaper).all()
        ret = []
        query.reverse()
        
        for query in query:
            ret.append(NewspaperApi(query.file_datetime, f"pub_{query.file_datetime}.pdf", url_for("newspaper_pages.view_pub", date_time=query.file_datetime), url_for("newspaper_pages.download_pub", date_time=query.file_datetime), query.id, query.date, query.credits).__dict__)
        
        return ret
    
    elif filter == "date" and query:
        query = db.session.query(Newspaper).filter_by(date=bleach.clean(query.replace("-", "/"))).first()
        
        if query:
            return NewspaperApi(query.file_datetime, f"pub_{query.file_datetime}.pdf", url_for("newspaper_pages.view_pub", date_time=query.file_datetime), url_for("newspaper_pages.download_pub", date_time=query.file_datetime), query.id, query.date, query.credits).__dict__
        
        else:
            return {}
    
    elif filter == "pub_num" and query:
        query = db.session.query(Newspaper).filter_by(id=bleach.clean(query)).first()
        
        if query:
            return NewspaperApi(query.file_datetime, f"pub_{query.file_datetime}.pdf", url_for("newspaper_pages.view_pub", date_time=query.file_datetime), url_for("newspaper_pages.download_pub", date_time=query.file_datetime), query.id, query.date, query.credits).__dict__
        
        else:
            return {}
    
    abort(404)