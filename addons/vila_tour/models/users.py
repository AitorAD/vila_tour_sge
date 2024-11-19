# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Users (models.Model):
    _name = "users"

    id = fields.Integer(string="ID", required=True)
    username = fields.Char(string="Username", required=True, unique=True)  # Nombre de usuario único
    email = fields.Char(string="Email", required=True)  # Email del usuario
    name = fields.Char(string="First Name", required=True)  # Nombre del usuario
    surname = fields.Char(string="Last Name", required=True)  # Apellido
    password = fields.Char(string="Password", required=True)  # Contraseña
    profile_picture = fields.Image(string="Profile Picture")  # Imagen para la foto de perfil
    role = fields.Selection(  # Rol del usuario con opciones predefinidas
        string="Role",
        selection=[
            ('USER', 'USER'),
            ('ADMIN', 'ADMIN'),
            ('EDITOR', 'EDITOR'),
        ],
        default='viewer',
        required=True
    )
    
    festival_ids = fields.One2many(
        comodel_name='festivals',
        inverse_name='creator_id',
        string='Festivals Created'
    )

    places_ids = fields.One2many(
        comodel_name='places',
        inverse_name='creator_id',
        string='Places Created'
    )

    recipes_ids = fields.One2many(
        comodel_name='recipes',
        inverse_name='creator_id',
        string='Recipes Created'
    )