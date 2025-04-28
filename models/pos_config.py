from xlwt.ExcelFormulaLexer import false_pattern

from odoo import api, fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    def switch_pos_picking_type(self, operation_type_id):
        self.ensure_one()
        if self.picking_type_id == operation_type_id:
            return self.picking_type_id.name
        operation = self.env['stock.picking.type'].search([('id', '=', operation_type_id)])
        if not operation:
            return False
        self.picking_type_id = operation.id
        return self.picking_type_id.name