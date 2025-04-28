# -*- coding: utf-8 -*-
# from odoo import http


# class PosMultiWarehouse(http.Controller):
#     @http.route('/pos_multi_warehouse/pos_multi_warehouse', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_multi_warehouse/pos_multi_warehouse/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_multi_warehouse.listing', {
#             'root': '/pos_multi_warehouse/pos_multi_warehouse',
#             'objects': http.request.env['pos_multi_warehouse.pos_multi_warehouse'].search([]),
#         })

#     @http.route('/pos_multi_warehouse/pos_multi_warehouse/objects/<model("pos_multi_warehouse.pos_multi_warehouse"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_multi_warehouse.object', {
#             'object': obj
#         })

