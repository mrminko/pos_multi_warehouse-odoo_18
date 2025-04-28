from odoo import fields, models, api

class PickingType(models.Model):
    _inherit = "stock.picking.type"

    pos_operation = fields.Boolean('POS Operation', help="Check if it is operation used in POS")
