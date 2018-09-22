import gi
import datetime
from BillingTab import *
from RecordsTab import *
from DatabaseWindow import *
from Bill import *
from Item import *
from Customer import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk

class MainApplication(Gtk.Window):

	def __init__(self, *args, **kwargs):
		Gtk.Window.__init__(self, title = "Chandan Snacks King")

		box = Gtk.VBox(False, 5)
		self.add(box)

		top_box = Gtk.HBox(False, 0)
		box.pack_start(top_box, False, False, 0)
		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename="1.jpg",
			width=800,
			height=-1,
			preserve_aspect_ratio=True)
		logo = Gtk.Image.new_from_pixbuf(pixbuf)
		top_box.pack_start(logo, True, True, 0)

		self.notebook = Gtk.Notebook()
		box.pack_start(self.notebook, False, False, 0)

		billing = BillingTab()
		self.notebook.append_page(billing, Gtk.Label("Billing"))

		records = RecordsTab()
		self.notebook.append_page(records, Gtk.Label("Records"))

		database_window = DatabaseWindow()
		self.notebook.append_page(database_window, Gtk.Label("Edit Database"))

win = MainApplication()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
win.set_size_request(800, 500)
Gtk.main()
