# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re

class Users(models.Model):
    _name = "users"
    _inherit = ['image.mixin']

    name = fields.Char(string="Username", required=True)
    password = fields.Char(string="Password", required=True)
    password_rep = fields.Char(string="Confirm Password", required=True)
    role = fields.Selection(
        selection=[
            ('Administrador', 'Administrador'),
            ('Redactor', 'Redactor'),
            ('Usuario', 'Usuario'),
        ],
        string='Role',
        required=True
    )
    email = fields.Char(string="Email", required=True)
    full_name = fields.Char(string="Full Name")
    birth_date = fields.Date(string="Birth Date")
    gender = fields.Char(string="Gender")
    phone = fields.Char(string="Phone", default=None)
    locality = fields.Char(string="Locality")
    zip_code = fields.Char(string="Postal Code", default=None)
    image_1920 = fields.Image(string="Profile Picture")
    last_modified = fields.Datetime(
        string="Last Modified",
        readonly=True,
        default=lambda self: fields.Datetime.now()
    )

    partner_id = fields.Many2one('res.partner', string='Contact')

    # Relational fields
    festival_ids = fields.One2many(
        comodel_name='festivals',
        inverse_name='creator_id',
        string='Festivals Created'
    )

    places_ids = fields.One2many(
        comodel_name='places',
        inverse_name='creator_id',
        string='Places Created',
        help='Places created by the user'
    )

    recipes_ids = fields.One2many(
        comodel_name='recipes',
        inverse_name='creator_id',
        string='Recipes Created'
    )

    _sql_constraints = [
        ('unique_username', 'unique(name)', 'The username must be unique.'),
    ]

    @api.constrains('phone', 'zip_code')
    def _check_numeric(self):
        for record in self:
            if record.phone:
                phone = record.phone.replace(" ", "")
                if not re.match(r'^\d+$', phone):
                    raise ValidationError('The phone number can only contain digits.')
            if record.zip_code:
                zip_code = record.zip_code.replace(" ", "")
                if not re.match(r'^\d+$', zip_code):
                    raise ValidationError('The postal code can only contain digits.')
                if len(zip_code) != 5:
                    raise ValidationError('The postal code must be exactly 5 characters long.')

    @api.constrains('password', 'password_rep')
    def _check_passwords_match(self):
        for record in self:
            if record.password != record.password_rep:
                raise ValidationError("Passwords do not match.")
            password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
            if not re.match(password_regex, record.password):
                raise ValidationError(
                    "The password must have at least 8 characters, include an uppercase letter, a lowercase letter, and a number."
                )

    @api.model
    def create(self, vals):
        record = super(Users, self).create(vals)

        partner = self.env['res.partner'].create({
            'name': vals.get('name'),
            'email': vals.get('email'),
            'phone': vals.get('phone'),
            'city': vals.get('locality'),
            'zip': vals.get('zip_code'),
            'image_1920': vals.get('image_1920'),
        })

        record.partner_id = partner.id

        user_vals = {
            'name': vals.get('name'),
            'login': vals.get('email'),
            'password': vals.get('password'),
            'email': vals.get('email'),
            'partner_id': partner.id,
            'active': True,
        }

        role = vals.get('role')
        if role:
            group = None
            if role == 'Administrador':
                group = self.env.ref('base.group_system')
            elif role == 'Redactor':
                group = self.env.ref('base.group_user')
            elif role == 'Usuario':
                group = self.env.ref('base.group_portal')

            if group:
                user_vals['groups_id'] = [(6, 0, [group.id])]

        self.env['res.users'].create(user_vals)

        tag_name = vals.get('role')
        if tag_name:
            tag = self.env['res.partner.category'].search([('name', '=', tag_name)], limit=1)
            if not tag:
                tag = self.env['res.partner.category'].create({'name': tag_name})
            partner.write({'category_id': [(4, tag.id)]})

        return record

    def write(self, vals):
        for record in self:
            if record.partner_id:
                if 'name' in vals:
                    record.partner_id.write({'name': vals['name']})
                if 'email' in vals:
                    record.partner_id.write({'email': vals['email']})
                if 'phone' in vals:
                    record.partner_id.write({'phone': vals['phone']})
                if 'locality' in vals:
                    record.partner_id.write({'city': vals['locality']})
                if 'zip_code' in vals:
                    record.partner_id.write({'zip': vals['zip_code']})
                if 'image_1920' in vals:
                    record.partner_id.write({'image_1920': vals['image_1920']})

            user = self.env['res.users'].search([('partner_id', '=', record.partner_id.id)], limit=1)
            if user:
                user_vals = {}
                if 'name' in vals:
                    user_vals['name'] = vals['name']
                if 'email' in vals:
                    user_vals['login'] = vals['email']
                    user_vals['email'] = vals['email']
                if 'password' in vals:
                    user_vals['password'] = vals['password']
                if user_vals:
                    user.write(user_vals)

                if 'role' in vals:
                    user.groups_id = [(5, 0, 0)]
                    new_group = None
                    if vals['role'] == 'Administrador':
                        new_group = self.env.ref('base.group_system')
                    elif vals['role'] == 'Redactor':
                        new_group = self.env.ref('base.group_user')
                    elif vals['role'] == 'Usuario':
                        new_group = self.env.ref('base.group_portal')

                    if new_group:
                        user.groups_id = [(6, 0, [new_group.id])]

        return super(Users, self).write(vals)

    def unlink(self):
        for record in self:
            user = self.env['res.users'].search([('partner_id', '=', record.partner_id.id)], limit=1)
            if user:
                user.unlink()

            if record.partner_id:
                record.partner_id.unlink()

        return super(Users, self).unlink()