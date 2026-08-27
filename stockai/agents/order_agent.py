from stockai.core.models import SKUInventoryItem, DemandForecast, PurchaseOrderDraft

class OrderAgent:
    """
    OrderAgent: Automatically composes vendor purchase orders and multi-currency supplier reorder emails.
    """
    def __init__(self):
        self.name = "OrderAgent"
        self.version = "1.0.0"

    def draft_purchase_order(self, item: SKUInventoryItem, forecast: DemandForecast) -> PurchaseOrderDraft:
        qty = forecast.recommended_reorder_quantity
        total = round(qty * item.unit_cost_usd, 2)
        po_num = f"PO-{abs(hash(item.sku)) % 100000:05d}"
        
        email_subj = f"URGENT PO {po_num}: Replenishment Order for {item.item_name} ({item.sku})"
        email_body = (
            f"Dear {item.vendor_name} Sales Operations,\n\n"
            f"Please accept this automated purchase order {po_num} for inventory replenishment.\n\n"
            f"• SKU: {item.sku}\n"
            f"• Item Description: {item.item_name}\n"
            f"• Quantity: {qty} Units\n"
            f"• Agreed Unit Price: ${item.unit_cost_usd:.2f} USD\n"
            f"• Total PO Amount: ${total:.2f} USD\n"
            f"• Target Delivery Window: {item.lead_time_days} Business Days\n\n"
            f"Please confirm receipt and dispatch tracking details at your earliest convenience.\n\n"
            f"Sincerely,\n"
            f"StockAI Autonomous Supply Chain Procurement System\n"
            f"Enterprise Inventory Management Desk"
        )

        return PurchaseOrderDraft(
            po_number=po_num,
            sku=item.sku,
            item_name=item.item_name,
            order_quantity=qty,
            unit_price_usd=item.unit_cost_usd,
            total_amount_usd=total,
            vendor_name=item.vendor_name,
            vendor_email=item.vendor_email,
            email_subject=email_subj,
            email_body_draft=email_body,
            estimated_delivery_days=item.lead_time_days
        )
