# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class pos_multi_warehouse(models.Model):
#     _name = 'pos_multi_warehouse.pos_multi_warehouse'
#     _description = 'pos_multi_warehouse.pos_multi_warehouse'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

