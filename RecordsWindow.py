import gi
import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
from collections import Counter
from DatabaseOperations import *

month_dict = {1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May', 6 : 'June', 7 : 'July',
			 8 : 'August', 9 : 'September', 10 : 'October', 11 : 'November', 12 : 'December'}

class RecordsWindow(Gtk.Dialog):

	def __init__(self, start_date, end_date, record_type):
		Gtk.Dialog.__init__(self, record_type + " Record Details", None, 0,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

		self.set_default_size(800, 300)

		scroll = Gtk.ScrolledWindow()
		middle_box = Gtk.Box()
		scroll.add_with_viewport(middle_box)
		scroll.set_size_request(800, 300)
		records_dict = self.get_records(start_date, end_date, record_type)

		record_tree_store = Gtk.TreeStore(str, int, int, int, int, int)
		for date, total in records_dict.items():
			piter = record_tree_store.append(None, [date, total[0], total[1], total[2], total[3], total[4]])
			for item, count in total[5].items():
				record_tree_store.append(piter, [item, count, 0, 0, 0, 0])

		self.record_tree_view = Gtk.TreeView(record_tree_store)
		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Time", renderer, text = 0)
		column.set_min_width(300)
		self.record_tree_view.append_column(column)
		column = Gtk.TreeViewColumn("Cash", renderer, text = 1)
		column.set_min_width(100)
		self.record_tree_view.append_column(column)
		column = Gtk.TreeViewColumn("Card", renderer, text = 2)
		column.set_min_width(100)
		self.record_tree_view.append_column(column)
		column = Gtk.TreeViewColumn("Online", renderer, text = 3)
		column.set_min_width(100)
		self.record_tree_view.append_column(column)
		column = Gtk.TreeViewColumn("Swiggy", renderer, text = 4)
		column.set_min_width(100)
		self.record_tree_view.append_column(column)
		column = Gtk.TreeViewColumn("Total", renderer, text = 5)
		column.set_min_width(100)
		self.record_tree_view.append_column(column)
		middle_box.pack_start(self.record_tree_view, False, False, 0)
		box = self.get_content_area()
		box.add(scroll)
		self.show_all()

	def get_records(self, start_date, end_date, record_type):
		"""
		Returns the records based
			Args:
				param1 (str): Start date
				param2 (str): End date
				param3 (str): Record Type
			Return:
				Returns a Dictionary of the records from database
		"""
		db = DatabaseOperations()
		records_dict = db.get_records(start_date, end_date)

		if record_type == "Daily":
			return records_dict

		monthly_record = {}

		for date, total in records_dict.items():
			date_time = datetime.datetime.strptime(date, "%d/%m/%Y")
			month = month_dict[date_time.month]+"-"+str(date_time.year)
			if month in monthly_record:
				temp_list = total
				old_list = monthly_record.get(month)

				cash_new_total = temp_list[0] + old_list[0]
				card_new_total = temp_list[1] + old_list[1]
				online_new_total = temp_list[2] + old_list[2]
				swiggy_new_total = temp_list[3] + old_list[3]
				new_total = temp_list[4] + old_list[4]

				old_item_count = old_list[5]
				new_item_count = temp_list[5]
				updated_item_count = dict(Counter(old_item_count) + Counter(new_item_count))
				monthly_record[month] = [cash_new_total, card_new_total, online_new_total, online_new_total, new_total, updated_item_count]
			else:
				temp_list = [total[0], total[1], total[2], total[3], total[4], total[5]]
				monthly_record[month] = temp_list
		return monthly_record
