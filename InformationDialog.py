import gi
import datetime
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
from DatabaseOperations import *

class InformationDialog(Gtk.MessageDialog):
	""" 
	This class is for display general information and error messages.
	"""
	def __init__(self, message, info):
		dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
			Gtk.ButtonsType.OK, message)
		dialog.format_secondary_text(info)
		dialog.set_default_size(300, 100)
		dialog.show_all()
		dialog.run()
		dialog.destroy()