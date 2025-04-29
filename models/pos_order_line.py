from odoo import api, fields, models

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    from_location = fields.Many2one("stock.location", string="From Location")