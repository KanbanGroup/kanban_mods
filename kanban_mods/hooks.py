app_name = "kanban_mods"
app_title = "Kanban Mods"
app_publisher = "Kevin Salt"
app_description = "Modifications and additions to Kanban ERP system"
app_email = "kevin@sound-and-spirit.nl"
app_license = "GNU General Public License (v3)"
app_icon = "fa fa-th"
app_color = "#e74c3c"
app_logo_url = "/files/Kanban_logo_large.png"

website_context = {
    "favicon": "/assets/erpnext/images/erpnext-favicon.svg",
#   "splash_image": "/assets/erpnext/images/erpnext-logo.png",
    "splash_image": "/files/Kanban_logo_large.png",
}
email_brand_image = "/files/Kanban_logo_large.png"


# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "kanban_mods",
# 		"logo": "/assets/kanban_mods/logo.png",
# 		"title": "Kanban Mods",
# 		"route": "/kanban_mods",
# 		"has_permission": "kanban_mods.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [ 
    "/assets/kanban_mods/css/desk/desktop_mods.css"
    ]
# app_include_js = "/assets/kanban_mods/js/kanban_mods.js"

# include js, css files in header of web template
# web_include_css = "/assets/kanban_mods/css/kanban_mods.css"
# web_include_js = "/assets/kanban_mods/js/kanban_mods.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "kanban_mods/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "kanban_mods/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Routing Rules

website_route_rules = [
{"from_route": "/quotations", "to_route": "Quotation"},
	{
		"from_route": "/quotations/<path:name>",
		"to_route": "order",
		"defaults": {
			"doctype": "Quotation",
			"parents": [{"label": "Quotations", "route": "quotations"}],
		},
	},
{"from_route": "/clientrfq", "to_route": "ClientRFQ"},
	{
		"from_route": "/clientrfq/<path:name>",
		"to_route": "clientrfq",
		"defaults": {
			"doctype": "ClientRFQ",
			"parents": [{"label": "Client RFQ", "route": "clientrfq"}],
		},
	},
]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "kanban_mods.utils.jinja_methods",
# 	"filters": "kanban_mods.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "kanban_mods.install.before_install"
# after_install = "kanban_mods.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "kanban_mods.uninstall.before_uninstall"
# after_uninstall = "kanban_mods.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "kanban_mods.utils.before_app_install"
# after_app_install = "kanban_mods.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "kanban_mods.utils.before_app_uninstall"
# after_app_uninstall = "kanban_mods.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "kanban_mods.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_whitelisted_methods = {
	"erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_quotation": "kanban_mods.kanban_mods.overrides.supplier_quotation.custom_make_quotation"
 }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
        # 15 minutes
        "0/15 * * * *": [
            "frappe.oauth.delete_oauth2_data",
            "frappe.website.doctype.web_page.web_page.check_publish_status",
            "frappe.twofactor.delete_all_barcodes_for_users",
            "frappe.email.doctype.email_account.email_account.notify_unreplied",
            "frappe.utils.global_search.sync_global_search",
            "frappe.deferred_insert.save_to_db",
        ],

        # every minute
         "* * * * *": [
            "frappe.email.queue.flush",
            "frappe.email.doctype.email_account.email_account.pull",
        ],

        # every 5 minutes
         "*/5 * * * *": [
 		    "frappe.monitor.flush",
		    "frappe.automation.doctype.reminder.reminder.send_reminders",
      ],

        # Hourly but offset by 30 minutes
        "30 * * * *": [
            "frappe.core.doctype.prepared_report.prepared_report.expire_stalled_report",
        ],

        # Daily but offset by 45 minutes
        "45 0 * * *": [
            "frappe.core.doctype.log_settings.log_settings.run_log_clean_up",
        ],
    },
	"all": [
	],

#  	"all": [
# 		"kanban_mods.tasks.all"
# 	],
# 	"daily": [
# 		"kanban_mods.tasks.daily"
# 	],
# 	"hourly": [
# 		"kanban_mods.tasks.hourly"
# 	],
# 	"weekly": [
# 		"kanban_mods.tasks.weekly"
# 	],
# 	"monthly": [
# 		"kanban_mods.tasks.monthly"
}

# Testing
# -------

# before_tests = "kanban_mods.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "kanban_mods.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "kanban_mods.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["kanban_mods.utils.before_request"]
# after_request = ["kanban_mods.utils.after_request"]

# Job Events
# ----------
# before_job = ["kanban_mods.utils.before_job"]
# after_job = ["kanban_mods.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"kanban_mods.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

