#  ICS News Website database module.
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
Database module for the ICS News Website.

This module contains all of the database models.
"""


# ------- Libraries and utils -------
import json
from flask import Blueprint, flash, render_template, request
from flask_security import RoleMixin, SQLAlchemySessionUserDatastore, UserMixin
from init import db, log


# ------- Blueprint init -------
database = Blueprint("database", __name__)


# ------- Temporary page route -------
# @database.route("/blog-db-add", methods=["GET", "POST"])
# @database.route("/newspaper-db-add", methods=["GET", "POST"])


# ------- Database models -------

# -=-=-= Accounts database =-=-=-
# ---- User roles table ----
roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
                       db.Column("role_id", db.Integer(), db.ForeignKey("role.id")), 
                       bind_key="accounts")


# ---- Roles table ----
class Role(db.Model, RoleMixin):
    __bind_key__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# ---- User table ----
class User(db.Model, UserMixin):
    __bind_key__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    pp_url = db.Column(db.String(255), default="img/logos/default_pp.png")
    password = db.Column(db.String(255), nullable=False)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic"))
    tf_phone_number = db.Column(db.String(128), nullable=True)
    tf_primary_method = db.Column(db.String(64), nullable=True)
    tf_totp_secret = db.Column(db.String(255), nullable=True)


# -=-=-= General database =-=-=-
# ---- School updates table ----
class SchoolUpdates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_time = db.Column(db.String(30))
    body = db.Column(db.String(4500))

    def __init__(self, title: str, date_time: str, body: str):
        self.title = title
        self.date_time = date_time
        self.body = body


# ------- Flask-Security user datastore -------
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
