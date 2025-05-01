/** @odoo-module */

import {patch} from "@web/core/utils/patch";
import {PosOrderline} from "@point_of_sale/app/models/pos_order_line";

patch(PosOrderline, {
    extraFields: {
        ...(PosOrderline.extraFields || {}),
        from_location: {
            model: "pos.order.line",
            name: "from_location",
            relation: "stock.location",
            type: "many2one",
            local: false,
        }
    }
})

patch(PosOrderline.prototype, {
    setup(vals) {
        super.setup(vals);
        if(this.product_id) {
            this.attachWarehouseLocation(vals);
        }
    },

    can_be_merged_with(orderline) {
        let result = super.can_be_merged_with(orderline);
        return result && this.raw.from_location.id === orderline.from_location;
    },

    attachWarehouseLocation(vals) {
        this.raw.from_location = {id:vals.from_location}
    }
});
