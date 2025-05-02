from odoo import api, fields, models

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    from_location = fields.Many2one("stock.location", string="From Location")

    #add field to load into pos frontend
    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super(PosOrderLine, self)._load_pos_data_fields(config_id)
        return fields + ['from_location']