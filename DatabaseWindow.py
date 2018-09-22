import gi
import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
from DatabaseOperations import *
from InformationDialog import *
from BillingSoftwareUtility import *
from BillingTab import *

class DatabaseWindow(Gtk.VBox):

	def __init__(self, *args, **kwargs):
		super(DatabaseWindow, self).__init__(*args, **kwargs)

		utility = BillingSoftwareUtility()
		liststore = Gtk.ListStore(int, str)
		liststore.append([1, "Add New Item"])
		liststore.append([2, "Edit Item Details"])

		top_box = Gtk.HBox(False, 10)
		self.pack_start(top_box, False, False, 10)

		label = Gtk.Label("Select Operation:")
		operation_box = Gtk.ComboBox.new_with_model_and_entry(liststore)
		operation_box.set_entry_text_column(1)

		top_box.pack_start(label, False, False, 10)
		top_box.pack_start(operation_box, False, False, 0)

		add_vbox = Gtk.VBox(False, 10)
		self.pack_start(add_vbox, False, False, 0)

		box_1 = Gtk.HBox(False, 10)
		add_vbox.pack_start(box_1, False, False, 10)

		label = Gtk.Label("Item Code:")
		self.item_code = Gtk.Entry()
		self.item_code.connect("changed", utility.insert_only_number)
		box_1.pack_start(label, False, False, 10)
		box_1.pack_start(self.item_code, False, False, 15)

		box_2 = Gtk.HBox(False, 10)
		add_vbox.pack_start(box_2, False, False, 10)

		label = Gtk.Label("Item Name:  ")
		self.item_name = Gtk.Entry()
		box_2.pack_start(label, False, False, 10)
		box_2.pack_start(self.item_name, False, False, 5)

		box_3 = Gtk.HBox(False, 10)
		add_vbox.pack_start(box_3, False, False, 10)

		label = Gtk.Label("Item Price:  ")
		self.item_price = Gtk.Entry()
		self.item_price.connect("changed", utility.insert_only_number)
		box_3.pack_start(label, False, False, 10)
		box_3.pack_start(self.item_price, False, False, 10)

		bottom_box = Gtk.HBox(False, 10)
		add_vbox.pack_start(bottom_box, False, False, 10)

		get_button = Gtk.Button("Submit")
		get_button.connect("clicked", self.process_request, operation_box)
		clear_button = Gtk.Button("Clear")
		clear_button.connect("clicked", self.clear_input_fields)
		bottom_box.pack_start(get_button, False, False, 10)
		bottom_box.pack_start(clear_button, False, False, 10)

	def process_request(self, button, operation_box):
		"""
		Process requests of adding or editing the database
			Args:
				param1 (Gtk.Button): Button to trigger the function
				param2 (Gtk.ComboBox): Combobox of the options
		"""

		item_code = int(self.item_code.get_text())
		item_name = self.item_name.get_text()
		item_price = int(self.item_price.get_text())
		db = DatabaseOperations()
		tree_iter = operation_box.get_active_iter()
		model = operation_box.get_model()
		operation = int(model[tree_iter][0])
		if operation == 1:
			try:
				billingTab = BillingTab()
				billingTab.add_item_to_list([item_code, item_name, item_price])
				result = db.add_new_item([item_code, item_name, item_price])
				InformationDialog("New Item Added Successfully", "Item Code:"+str(item_code))
			except Exception as e:
				dialog = InformationDialog("Error Adding New Item", "Item Code:"+str(item_code)+" already exist")
				print(e)
		elif operation == 2:
			try:
				db.edit_item([item_code, item_name, item_price])
				InformationDialog("Item Edited Successfully", "Item Code:"+str(item_code))
			except Exception as e:
				InformationDialog("Operation Failed", "Give Proper Details")
				print(e)
		self.clear_input_fields()

	def clear_input_fields(self, *args):
		utility = BillingSoftwareUtility()
		utility.clear_input_fields(self.item_code, self.item_name, self.item_price)
