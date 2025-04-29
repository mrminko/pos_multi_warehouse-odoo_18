/** @odoo-module */

import {patch} from "@web/core/utils/patch";
import {PosOrderline} from "@point_of_sale/app/models/pos_order_line";

patch(PosOrderline.prototype, {
    setup(vals) {
        super.setup(vals);
        if(this.product_id) {
            this.attachWarehouseLocation();
        }
    },
    can_be_merged_with(orderline) {
        let result = super.can_be_merged_with(orderline);
        return result && this.from_location_id ==
    },

    attachWarehouseLocation() {
        this.from_location_id = this.pos.from_location_id
    }
});
