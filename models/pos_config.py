from odoo import api, fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    def switch_pos_picking_type(self, operation_type_id):
        self.ensure_one()
        if self.picking_type_id == operation_type_id:
            return {"from_location": {"id": self.picking_type_id.default_location_src_id.id}, "name":self.picking_type_id.name}
        operation = self.env['stock.picking.type'].search([('id', '=', operation_type_id)])
        if not operation:
            return False
        self.picking_type_id = operation.id
        result = {"from_location": {"id": self.picking_type_id.default_location_src_id.id}, "name":self.picking_type_id.name}
        return result
