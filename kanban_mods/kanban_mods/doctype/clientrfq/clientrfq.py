# Copyright (c) 2024, Kevin Salt and contributors
# For license information, please see license.txt

import json

import frappe
import inspect
from frappe import _
from frappe.core.doctype.communication.email import make
from frappe.desk.form.load import get_attachments
from frappe.model.mapper import get_mapped_doc
from frappe.utils import get_url
from frappe.utils.print_format import download_pdf
from frappe.utils.user import get_user_fullname
from frappe.model.document import Document
from frappe.contacts.address_and_contact import load_address_and_contact

form_grid_templates = {"items": "templates/form_grid/item_grid.html"}

from datetime import date
from kanban_mods.utils.misc_functions import dump

STANDARD_USERS = ("Guest", "Administrator", "Customer")

class ClientRFQ(Document):

	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from kanban_mods.kanban_mods.doctype.clientrfq_item import (
			ClientRFQ_Item
		)
		
		amended_from: DF.Link | None
		billing_address: DF.link | None
		billing_address_display: DF.SmallText | None
		client: DF.Link
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

	def on_create(self):
		self.set_initial_values();
	
	def set_initial_values(self):
		self.email_template = "ClientRFQ_Email"
		self.letter_head = "New_Kanban_Letterhead"
		self.naming_series = "SAL-CRFQ-.YYYY.-"
		self.send_attached_files = 0
		self.send_document_print = 1
		self.status = "Draft"
		self.transaction_date = date.today()
		self.vendor = "Kanban-Group Bearings"

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
		self.send_to_client()
		self.create_supplier_RFQ()
		
	def get_link(self):
		# RFQ link for suppliecustomerr portal
		route = frappe.db.get_value(
			"Portal Menu Item", {"reference_doctype": "ClientRFQ"}, ["route"]
		)
		if not route:
			frappe.throw(_("Please add Client RFQs the sidebar in Portal Settings."))

		return get_url(f"{route}/{self.name}")

	def send_to_client(self):
		client = frappe.get_doc("Customer", self.client)
		if client.email_id is not None:
			self.validate_email_id(client)

			self.rfq_mail(client)
			client.email_sent = 1
			client.save()

	def validate_email_id(self, args):
		if not args.email_id:
			frappe.throw(
				("Row {0}: For Client {1}, Email Address is Required to send an email").format(
					args.idx, frappe.bold(args.email_id)
				)
			)
	
	def rfq_mail(self, client, preview=False):
		client_email_id = client.get("email_id")
		full_name = get_user_fullname(client_email_id)
		if full_name == "Guest":
			full_name = "Administrator"

		doc_args = self.as_dict()

		if client.get("contact"):
			contact = frappe.get_doc("Contact", client_email_id)
			doc_args["contact"] = contact.as_dict()

		doc_args.update(
			{
				"vendor": self.get("vendor"),
				"vendor_name": self.get("vendor_name"),
				"contact_name": full_name,
			}
		)

		if not self.email_template:
			return

		email_template = frappe.get_doc("Email Template", self.email_template)
		message = frappe.render_template(email_template.response_, doc_args)
		subject = frappe.render_template(email_template.subject, doc_args)
		sender_list = frappe.get_all("Email Account", {"default_outgoing": 1}, "email_id")

		if not sender_list or len(sender_list) != 1:
			sender = "sales@kanban-group.com"
		else:
			sender = sender_list[0].email_id

		if preview:
			return {"message": message, "subject": subject}

		attachments = []
		if self.send_document_print:
			supplier_language = frappe.db.get_value("Customer", self.client, "language")
			system_language = frappe.db.get_single_value("System Settings", "language")
			attachments.append(
				frappe.attach_print(
					self.doctype,
					self.name,
					doc=self,
					print_format=self.meta.default_print_format or "Standard",
					lang=supplier_language or system_language,
					letterhead=self.letter_head,
				)
			)

		self.send_email(client, sender, subject, message, attachments)

	def send_email(self, data, sender, subject, message, attachments):

		make(
			subject=subject,
			content=message,
			recipients=data.email_id,
			sender=sender,
			attachments=attachments,
			send_email=True,
			doctype=self.doctype,
			name=self.name,
		)["name"]

		frappe.msgprint(_("Email Sent to Client --- {0}").format(self.client))

	def create_supplier_RFQ(self):
		#########################################################
		# Since we are a drop shipping company, the faster we can 
		# get the Client RFQ processed the better. So ...
		#
		# This method automatically creates a draft supplier RFQ
		# Ready to be checked, updated and submitted by the staff
		#########################################################

		supplierRFQ = frappe.new_doc("Request for Quotation")
		# what is the minimum amount of data to be set up
		supplierRFQ.items = self.items
		supplierRFQ.naming_series = "PUR-RFQ-.YYYY.-"
		supplierRFQ.company = "Kanban-Group Bearings"
		supplierRFQ.billing_address = "Kanban-Group Bearings-Office"
		supplierRFQ.transaction_date = self.transaction_date
		supplierRFQ.schedule_date = self.schedule_date
		supplierRFQ.status = "Draft"
		supplierRFQ.email_template = "RFQ Email"
		supplierRFQ.send_attached_files = 0
		supplierRFQ.send_document_print = 1
		supplierRFQ.letter_head = "New_Kanban_Letterhead"
		supplierRFQ.items = create_item_list(self.items, self.schedule_date)
		supplierRFQ.suppliers = create_supplier_list()
		supplierRFQ.insert(ignore_permissions=True)


#############################################################
# End of the class itself .... the rest are utility methods #
#############################################################

def get_context(context):
	clientrfq_name = frappe.form_dict.name
	clientrfq = frappe.get_doc("ClientRFQ", clientrfq_name)
	context.clientrfq = clientrfq

def get_list_context(context=None):

	from kanban_mods.kanban_mods.controllers.website_list_for_clientrfq import get_list_context
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
			}
		},
		target_doc,
		set_missing_values,
		ignore_permissions=ignore_permissions,
	)

	return doclist

def create_item_list(items, req_date):
	new_items = []
	has_shipping = 0
	for it in items:
		#	check if there is an item with ID Shipping
		if it.item_code == "Shipping":
			has_shipping = 1

		# now make the Supplier RFQ Item list
		item = frappe.new_doc("Request for Quotation Item")

		item.item_code = it.item_code
		item.item_name = it.item_code
		item.schedule_date = req_date
		item.description = it.description
		item.item_group = it.item_group
		item.qty = it.qty
		item.stock_uom = it.uom
		item.uom = it.uom
		item.conversion_factor = 1
		item.stock_qty = it.qty
		item.warehouse = "Customer Direct Delivery - KB"

		new_items.append(item)

	if not has_shipping:
		new_items.append(create_shipping_item(req_date))

	return new_items
	

def create_supplier_list():
	# we always assume all suppliers shoud be offered the 
	# option to quote ... but even if this assumption is 
	# wrong, the buyer will be ablw to amend the list before 
	# submitting the document. so ....

	# get all the suppliers
	sup_list = frappe.get_all("Supplier",
						   fields=[
							   "name",
							   "supplier_primary_contact",
							   "supplier_name",
							   "email_id"
							]
						)
	suppliers = []
	# Add each supplier to the list
	for sup in sup_list:
		supplier = frappe.new_doc("Request for Quotation Supplier")
		supplier.supplier = sup.name
		supplier.contact = sup.supplier_primary_contact
		supplier.quote_status = "Pending"
		supplier.supplier_name = sup.supplier_name
		supplier.email_id = sup.email_id
		supplier.send_email = 1
		supplier.email_sent = 0
		suppliers.append(supplier)

	return suppliers


def create_shipping_item(req_date):

	ship_item = frappe.new_doc("Request for Quotation Item")
	ship_item.item_code = "Shipping"
	ship_item.item_name = "Shipping"
	ship_item.schedule_date = req_date
	ship_item.description = "Shipping"
	ship_item.item_group = "Transport"
	ship_item.qty = 1
	ship_item.stock_uom = "pkg"
	ship_item.uom = "pkg"
	ship_item.conversion_factor = 1
	ship_item.stock_qty = 1
	ship_item.warehouse = "Customer Direct Delivery - KB"

	return ship_item

