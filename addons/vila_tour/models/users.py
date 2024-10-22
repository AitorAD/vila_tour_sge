# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Users (models.Model):
    _name = "users"
    name = fields.Char()