# Copyright (c) 2024, Kevin Salt and contributors
# For license information, please see license.txt

import json

import frappe
from frappe import _
from frappe.core.doctype.communication.email import make
from frappe.desk.form.load import get_attachments
from frappe.model.mapper import get_mapped_doc
from frappe.utils import get_url
from frappe.utils.print_format import download_pdf
from frappe.utils.user import get_user_fullname
from frappe.model.document import Document

from erpnext.accounts.party import get_party_account_currency, get_party_details
from erpnext.buying.utils import validate_for_items

#from erpnext.controllers.buying_controller import BuyingController
#from kanban_mods.controllers.clientrfq.clientrfq_controller import ClientRFQController
from datetime import date

STANDARD_USERS = ("Guest", "Administrator")

class ClientRFQ(Document):

	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from kanban_mods.kanban_mods.doctype.clientrfq_item import (
			ClientRFQ_Item
		)
		
		from kanban_mods.kanban_mods.doctype.clientrfq_supplier import (
			ClientRFQ_Supplier
		)

		amended_from: DF.Link | None
		billing_address: DF.link | None
		billing_address_display: DF.SmallText | None
		company: DF.Link
		email_template: DF.Link 
		incoterm: DF.Link | None
		items: DF.Table[ClientRFQ_Item]
		letter_head: DF.Link 
		message_for_supplier: DF.TextEditor
		named_place: DF.Data | None
		naming_series: DF.Literal
		opportunity: DF.Link | None
		schedule_date: DF.Date | None
		select_print_heading: DF.Link | None
		send_attached_files: DF.Check | 1
		send_document_print: DF.Check | 0
		status: DF.Literal["Draft", "Submitted", "Cancelled"]
		tc_name: DF.Link | None
		terms: DF.TextEditor | None
		transaction_date: DF.Date 
		vendor: DF.Link 
		doctype: DF.Link | "ClientRFQ"

	def set_initial_values(self):
		self.email_template = "CustRFC_email"
		self.letter_head = "New_Kanban_Letterhead"
		self.naming_series = "SAL-CRFQ-.YYYY.-"
		self.send_attached_files = 1
		self.send_document_print = 0
		self.status = "Draft"
		self.transaction_date = date.today()
		self.vendor = "Kanban Group Bearings"

	def set_buyer_details(self, buyer):
		self.company = buyer
		self.billing_address = buyer.billing_address

	def validate(self):
		# validate_for_items(self)
		pass

		if self.docstatus < 1:
			# after amend and save, status still shows as cancelled, until submit
			self.db_set("status", "Draft")

	def on_submit(self):
		self.db_set("status", "Submitted")
		self.send_to_vendor()

	def send_to_vendor(self):
		supplier = self.vendor
		if supplier.email_id is not None and supplier.send_email:
			self.validate_email_id(supplier)
			update_password_link, contact = self.update_supplier_contact(supplier, self.get_link())
			self.update_supplier_part_no(supplier.supplier)
			self.supplier_rfq_mail(supplier, update_password_link, self.get_link())
			supplier.email_sent = 1
			supplier.save()

def get_context(context):
    clientrfq_name = frappe.form_dict.name
    clientrfq = frappe.get_doc("ClientRFQ", clientrfq_name)
    context.clientrfq = clientrfq

def get_list_context(context=None):
	from kanban_mods.kanban_mods.controllers.website_list_for_contact import get_list_context

	list_context = get_list_context(context)
	list_context.update(
		{
			"show_sidebar": True,
			"show_search": True,
			"no_breadcrumbs": True,
			"title": _("Client Requests for Quotations"),
		}
	)
	return list_context


def get_list(source_name):

	doclist = get_mapped_doc(
		"ClientRFQ",
		source_name,
		{
			"ClientRFQ": {"doctype": "ClientRFQ", "validation": {"docstatus": ["=", 1]}},
			"ClientRFQ Item": {
				"doctype": "ClientRFQ Item",
				"field_map": {"parent": "prevdoc_docname", "name": "clientrfcq_item"},
				"postprocess": update_item,
				"condition": can_map_row,
			},
		},
		target_doc,
		set_missing_values,
		ignore_permissions=ignore_permissions,
	)

	return doclist
