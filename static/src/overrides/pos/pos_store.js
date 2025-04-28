/** @odoo-module */

import {patch} from "@web/core/utils/patch";
import {PosStore} from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    async processServerData() {
        await super.processServerData();
        let wh = await this.env.services.orm.searchRead(
            "stock.picking.type",
            [['id', '=', this.config.picking_type_id.id]],
            ['name']
        )
        this.warehouse_name = wh[0].name;
    }
})