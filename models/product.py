from odoo import fields, models, api
from itertools import groupby
from operator import itemgetter
from datetime import date

class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_product_info_pos(self, price, quantity, pos_config_id):
        self.ensure_one()
        config = self.env['pos.config'].browse(pos_config_id)

        # Tax related
        taxes = self.taxes_id.compute_all(price, config.currency_id, quantity, self)
        grouped_taxes = {}
        for tax in taxes['taxes']:
            if tax['id'] in grouped_taxes:
                grouped_taxes[tax['id']]['amount'] += tax['amount']/quantity if quantity else 0
            else:
                grouped_taxes[tax['id']] = {
                    'name': tax['name'],
                    'amount': tax['amount']/quantity if quantity else 0
                }

        all_prices = {
            'price_without_tax': taxes['total_excluded']/quantity if quantity else 0,
            'price_with_tax': taxes['total_included']/quantity if quantity else 0,
            'tax_details': list(grouped_taxes.values()),
        }

        # Pricelists
        if config.use_pricelist:
            pricelists = config.available_pricelist_ids
        else:
            pricelists = config.pricelist_id
        price_per_pricelist_id = pricelists._price_get(self, quantity) if pricelists else False
        pricelist_list = [{'name': pl.name, 'price': price_per_pricelist_id[pl.id]} for pl in pricelists]

        #####
        quant = self.env['stock.quant'].search([
            ('product_id', '=', self.id),
            ('location_id', '=', config.picking_type_id.default_location_src_id.id)
        ])
        # Warehouses
        warehouse_list = [
            {'id': w.id,
            'name': w.name,
            # 'available_quantity': self.with_context({'warehouse_id': w.id}).qty_available,
            'available_quantity': quant.inventory_quantity_auto_apply,
            'forecasted_quantity': self.with_context({'warehouse_id': w.id}).virtual_available,
            'uom': self.uom_name}
            for w in self.env['stock.warehouse'].search([('company_id', '=', config.company_id.id)])]

        if config.picking_type_id.warehouse_id:
            # Sort the warehouse_list, prioritizing config.picking_type_id.warehouse_id
            warehouse_list = sorted(
                warehouse_list,
                key=lambda w: w['id'] != config.picking_type_id.warehouse_id.id
            )

        # Suppliers
        key = itemgetter('partner_id')
        supplier_list = []
        for key, group in groupby(sorted(self.seller_ids, key=key), key=key):
            for s in list(group):
                if not((s.date_start and s.date_start > date.today()) or (s.date_end and s.date_end < date.today()) or (s.min_qty > quantity)):
                    supplier_list.append({
                        'id': s.id,
                        'name': s.partner_id.name,
                        'delay': s.delay,
                        'price': s.price
                    })
                    break

        # Variants
        variant_list = [{'name': attribute_line.attribute_id.name,
                         'values': list(map(lambda attr_name: {'name': attr_name, 'search': '%s %s' % (self.name, attr_name)}, attribute_line.value_ids.mapped('name')))}
                        for attribute_line in self.attribute_line_ids]

        return {
            'all_prices': all_prices,
            'pricelists': pricelist_list,
            'warehouses': warehouse_list,
            'suppliers': supplier_list,
            'variants': variant_list
        }
