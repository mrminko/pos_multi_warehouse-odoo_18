from odoo import api, fields, models
from odoo.tools import formatLang

class PosOrder(models.Model):
    _inherit = 'pos.order'

    #return invoice name and amount_residual of a pos order
    def get_invoice_details(self):
        self.ensure_one()
        invoice = self.account_move
        amount_residual = formatLang(
            self.env, abs(invoice.amount_residual), currency_obj=invoice.currency_id),
        return {
            "id": invoice.id,
            "name": invoice.name,
            "amount_residual": amount_residual
        }
