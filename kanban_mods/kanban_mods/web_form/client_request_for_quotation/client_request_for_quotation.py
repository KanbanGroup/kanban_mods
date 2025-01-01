import json

import frappe
from frappe import _
from frappe.modules.utils import get_module_app
from frappe.utils import flt, has_common
from frappe.utils.user import is_website_user
from frappe.utils.user import get_user_fullname

from kanban_mods.utils.misc_functions import dump
from kanban_mods.kanban_mods.controllers import website_list_for_clientrfc as wl

@frappe.whitelist() 
def set_default_values(): 
	retval = {}
	user = frappe.session.user
	retval[f'user'] = user	
	retval[f'contact'] = get_user_fullname(user)
	
	if frappe.has_permission("ClientRFQ", "write", None,  user):

		client = wl.get_parents_for_user("Customer")[0]
		retval[f'client'] = client
		retval[f'status'] = "Submitted"
		customer = wl.get_doc("Customer", client)
		retval[f'billing_address'] = customer.customer_primary_address
		retval[f'billing_address_display'] = customer.primary_address
		retval[f'permitted'] = True
	else:
		retval[f'permitted'] = False
	return retval

@frappe.whitelist() 
def get_uom(item_code):
	return(frappe.db.get_value("Item", item_code, ["stock_uom"]))

	

def get_context(context):
	# do your magic here
	context.show_sidebar = True


