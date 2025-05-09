/** @odoo-module */

import {patch} from "@web/core/utils/patch";
import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { onWillStart } from "@odoo/owl";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup(...arguments);
        onWillStart(async () => {
            // super.onWillStart(...arguments)
            const order = this.pos.get_order();
            if (!order || !order._isRefundOrder()) {
                return;
            }
            const refund_id = order.lines[0].refunded_orderline_id.id
            const refund_order_id = order.lines[0].baseData[refund_id]?.order_id
            if (refund_order_id) {
                let invoice = await this.env.services.orm.call(
                    "pos.order",
                    "get_invoice_details",
                    [refund_order_id],
                )
                this.refund_invoice = invoice.name
                this.refund_invoice_amt_due = invoice.amount_residual
            }
        });
    }
})