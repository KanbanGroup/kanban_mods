#################################################################
# There is an issue with the auto create of a quotation via the #
# supplier quotation "Create From" button. The "rate" used in a #
# supplier quotation is automatically used to populate the sales#
# quotation, which results in a "first look" filled with errors #
# in the item pricing.                                          #
#                                                               #
# Because of our automated process of updating the price lists, #
# we need to add a function to correct the prices before it hits#
# the screen, so as not to cause confusion.                     #
#################################################################
# Author: Kevin Salt
# Last modified 21/01/2025
# See also: hooks.py - override_whitelisted_methods
#################################################################

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate

from kanban_mods.utils.misc_functions import dump

@frappe.whitelist()

def custom_make_quotation(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Supplier Quotation",
		source_name,
		{
			"Supplier Quotation": {
				"doctype": "Quotation",
				"field_map": {
					"name": "supplier_quotation",
				},
			},
			"Supplier Quotation Item": {
				"doctype": "Quotation Item",
				"condition": lambda doc: frappe.db.get_value("Item", doc.item_code, "is_sales_item") == 1,
				"add_if_empty": True,
			},
		},
		target_doc,
	)
	set_sales_item_prices(doclist)
	return(doclist)

def set_sales_item_prices(doc):
	for item in doc.items:
		dump(item)

''' 
This is the stuff I need to sort out

     item_code: 02872/2/02820/2/Q
	 price_list_rate: 100.0
     base_price_list_rate: 100.0
      discount_percentage: 0
     discount_amount: 0
     rate: 200.0
     net_rate: 200.0
     amount: 20000.0
     net_amount: 20000.0
     base_rate: 200.0
     base_net_rate: 200.0
     base_amount: 20000.0
     base_net_amount: 20000.0
	 
'''