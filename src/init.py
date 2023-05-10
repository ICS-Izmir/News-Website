#  ICS News Website application init file.
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


# ------- Libraries -------
import logging
import os
from flask import Flask, request, session
from flask_ckeditor import CKEditor
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from mailjet_rest import Client
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from config import AppConfig


# -=-=-= Functions =-=-=-

# ---- Custom locale selector for Babel ----
def localeselector():
    lang = session.get("lang")

    if lang:
        return lang

    session["lang"] = request.accept_languages.best_match(AppConfig.SUPPORTED_LANGS)
    return session.get("lang")


# ------- Flask and Flask plug-in init -------
app = Flask(__name__)
app.config.from_object(AppConfig)
ckeditor = CKEditor(app)
cache = Cache(app)
db = SQLAlchemy(app)
babel = Babel(app, locale_selector=localeselector)
csrf = CSRFProtect(app)
mailjet = Client(auth=(AppConfig.MAILJET_API_KEY, AppConfig.MAILJET_API_SECRET), version="v3.1")
ga = BetaAnalyticsDataClient()


# -=-=-= Logging init =-=-=-
formatter = logging.Formatter("[%(asctime)s] [%(threadName)s/%(levelname)s] [%(module)s/%(funcName)s]: %(message)s")

# ---- Get a logger with custom settings ----
def get_logger(name, log_file, level):
    handler = logging.FileHandler(os.path.join(AppConfig.LOG_FILE_PATH, log_file))        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


log = get_logger("main", "INPApp_MainPyLog.log", AppConfig.LOG_LEVEL)
debug_log = get_logger("debug", "INPApp_DebugPyLog.log", logging.DEBUG)