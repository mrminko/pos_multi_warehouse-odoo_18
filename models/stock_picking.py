from odoo import fields, models, api
from odoo.tools import groupby

class PickingType(models.Model):
    _inherit = "stock.picking.type"

    pos_operation = fields.Boolean('POS Operation', help="Check if it is operation used in POS")

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _has_different_location(self, lines):
        location = lines[0].from_location
        return any(l.from_location != location for l in lines[1:])

    def _prepare_different_location_stock_move_vals(self, lines):
        result = []
        for line in lines:
            result.append({
            'name': line.name,
            'product_uom': line.product_id.uom_id.id,
            'picking_id': self.id,
            'picking_type_id': self.picking_type_id.id,
            'product_id': line.product_id.id,
            'product_uom_qty': line.qty,
            'location_id': line.from_location.id,
            'location_dest_id': self.location_dest_id.id,
            'company_id': self.company_id.id,
            'never_product_template_attribute_value_ids': line.attribute_value_ids.filtered(lambda a: a.attribute_id.create_variant == 'no_variant'),
        })
        return result

    def _create_move_from_pos_order_lines(self, lines):
        print("=====_create_move_from_pos_order_lines", lines)
        self.ensure_one()
        lines_by_product = groupby(sorted(lines, key=lambda l: l.product_id.id), key=lambda l: l.product_id.id)
        move_vals = []
        for dummy, olines in lines_by_product:
            order_lines = self.env['pos.order.line'].concat(*olines)
            # print("=====order_lines", order_lines)
            if len(order_lines) > 1 and self._has_different_location(order_lines):
                v = self._prepare_different_location_stock_move_vals(order_lines)
                move_vals += v
                print("=====has_v", v)
            else:
                move_vals.append(self._prepare_stock_move_vals(order_lines[0], order_lines))
        # print("=====move_vals", move_vals)
        moves = self.env['stock.move'].create(move_vals)
        # print("=====moves", moves)
        confirmed_moves = moves._action_confirm()
        # print("=====confirmed_moves", confirmed_moves)
        confirmed_moves._add_mls_related_to_order(lines, are_qties_done=True)
        confirmed_moves.picked = True
        self._link_owner_on_return_picking(lines)
