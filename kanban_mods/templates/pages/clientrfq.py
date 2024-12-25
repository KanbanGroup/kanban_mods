
import frappe
from frappe import _

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	print(frappe.form_dict)
	exit()
	context.doc = frappe.get_doc(frappe.form_dict.doctype, frappe.form_dict.name)
	if hasattr(context.doc, "set_indicator"):
		context.doc.set_indicator()
	context.parents = frappe.form_dict.parents
	context.title = frappe.form_dict.name

	default_print_format = frappe.db.get_value(
		"Property Setter",
		dict(property="default_print_format", doc_type=frappe.form_dict.doctype),
		"value",
	)
	if default_print_format:
		context.print_format = default_print_format
	else:
		context.print_format = "Standard"
	if not frappe.has_website_permission(context.doc):
		frappe.throw(_("Not Permitted"), frappe.PermissionError)

	context.available_loyalty_points = 0.0
	context.show_pay_button = (False)
	context.show_make_pi_button = False

def get_attachments(dt, dn):
	return frappe.get_all(
		"File",
		fields=["name", "file_name", "file_url", "is_private"],
		filters={"attached_to_name": dn, "attached_to_doctype": dt, "is_private": 0},
	)
