import gi
import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
from DatabaseOperations import *
from RecordsWindow import *
from InformationDialog import *

class RecordsTab(Gtk.VBox):

	def __init__(self, *args, **kwargs):
		super(RecordsTab, self).__init__(*args, **kwargs)

		records_type_liststore = Gtk.ListStore(str)
		records_type_liststore.append(["Daily"])
		records_type_liststore.append(["Monthly"])

		top_box = Gtk.HBox(False, 10)
		self.pack_start(top_box, False, False, 10)

		label = Gtk.Label("Records Type:")
		records_type = Gtk.ComboBox.new_with_model_and_entry(records_type_liststore)
		records_type.set_entry_text_column(0)

		top_box.pack_start(label, False, False, 10)
		top_box.pack_start(records_type, False, False, 0)

		daily_box_1 = Gtk.HBox(False, 10)
		self.pack_start(daily_box_1, False, False, 10)

		label = Gtk.Label("Start Date:")
		self.start_date = Gtk.Entry()
		daily_box_1.pack_start(label, False, False, 10)
		daily_box_1.pack_start(self.start_date, False, False, 20)

		daily_box_2 = Gtk.HBox(False, 10)
		self.pack_start(daily_box_2, False, False, 10)

		label = Gtk.Label("End Date:  ")
		self.end_date = Gtk.Entry()
		daily_box_2.pack_start(label, False, False, 10)
		daily_box_2.pack_start(self.end_date, False, False, 20)

		bottom_box = Gtk.HBox(False, 10)
		self.pack_start(bottom_box, False, False, 10)

		get_button = Gtk.Button("Get Records")
		get_button.connect("clicked", self.get_records, records_type)
		clear_button = Gtk.Button("Clear")
		clear_button.connect("clicked", self.clear_input_fields)
		bottom_box.pack_start(get_button, False, False, 10)
		bottom_box.pack_start(clear_button, False, False, 10)

	def get_records(self, get_records_button, record_type_combobox):
		"""
		Displays a Gtk.Dialog of the records
			Args:
				param1 (Gtk.Button): Button to display records
				param2 (Gtk.ComboBox): Combobox containing the options
		"""
		start_date = self.start_date.get_text()
		end_date = self.end_date.get_text()
		tree_iter = record_type_combobox.get_active_iter()
		model = record_type_combobox.get_model()
		record_type = model[tree_iter][0]
		dialog = RecordsWindow(start_date, end_date, record_type)
		response = dialog.run()
		if response == Gtk.ResponseType.CANCEL:
			dialog.destroy()

	def clear_input_fields(self, *args):
		utility = BillingSoftwareUtility()
		utility.clear_input_fields(self.start_date, self.end_date)
