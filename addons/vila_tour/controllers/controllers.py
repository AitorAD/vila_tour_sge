# -*- coding: utf-8 -*-
# from odoo import http


# class VilaTour(http.Controller):
#     @http.route('/vila_tour/vila_tour', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vila_tour/vila_tour/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('vila_tour.listing', {
#             'root': '/vila_tour/vila_tour',
#             'objects': http.request.env['vila_tour.vila_tour'].search([]),
#         })

#     @http.route('/vila_tour/vila_tour/objects/<model("vila_tour.vila_tour"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vila_tour.object', {
#             'object': obj
#         })
