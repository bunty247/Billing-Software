import gi
import datetime
import time
from DatabaseOperations import *
from XLSWriterUtility import *
from InformationDialog import *
from BillingSoftwareUtility import *
from Bill import *
from Item import *
from Customer import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk

item_list_from_database = {}


class BillingTab(Gtk.VBox):

    def __init__(self, *args, **kwargs):
        super(BillingTab, self).__init__(*args, **kwargs)

        db = DatabaseOperations()
        utility = BillingSoftwareUtility()
        global item_list_from_database
        # Get all food items from database on application init
        item_list_from_database = db.get_all_items()
        self.item_list_for_bill = {}  # Dictionary for Bill Display
        self.total_amount = 0  # Total amount of the bill
        # Get Bill number from database
        self.bill_number_fromdb = int(db.get_and_update_bill_number_on_init())
        self.payment_mode = 'Cash'  # Default Payment Mode
        db.create_daily_record_entry()

        # Customer Container
        customer_container = Gtk.HBox(False, 10)
        self.pack_start(customer_container, False, False, 10)
        mobile_number_label = Gtk.Label("Mobile No: ")
        customer_name_label = Gtk.Label("Customer Name: ")
        reward_label = Gtk.Label("Reward Point: ")
        self.reward_count_label = Gtk.Label("0")
        self.customer_name_entry = Gtk.Entry()
        self.mobile_number_entry = Gtk.Entry()
        self.mobile_number_entry.connect(
            "key-press-event", self._key_pressed_customer)
        self.connect("key-press-event", self._key_pressed)
        self.mobile_number_entry.connect("changed", utility.insert_only_number)
        customer_container.pack_start(mobile_number_label, False, False, 10)
        customer_container.pack_start(
            self.mobile_number_entry, False, False, 10)
        customer_container.pack_start(customer_name_label, False, False, 0)
        customer_container.pack_start(
            self.customer_name_entry, False, False, 0)
        customer_container.pack_start(reward_label, False, False, 0)
        customer_container.pack_start(self.reward_count_label, False, False, 0)

        # Code and Name Container
        entry_container = Gtk.HBox(False, 10)
        self.pack_start(entry_container, False, False, 10)
        item_code_label = Gtk.Label("Item Code: ")
        self.item_code_entry = Gtk.Entry()
        self.item_code_entry.set_size_request(10, 20)
        self.item_code_entry.connect("key-press-event", self._key_pressed)
        self.connect("key-press-event", self._key_pressed)
        self.item_code_entry.connect("changed", utility.insert_only_number)
        # self.item_code_entry.connect("changed", self.show_items_popup)
        self.item_code_entry.grab_focus()

        self.popover = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.pack_start(Gtk.ModelButton("Item 1"), False, True, 10)
        vbox.pack_start(Gtk.Label("Item 2"), False, True, 10)
        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)

        item_name_label = Gtk.Label()
        item_name_label.set_markup(
            "Press <b>""+""</b> to add item to bill. Press <b>""Enter""</b> to finalize the Bill.")
        entry_container.pack_start(item_code_label, False, False, 10)
        entry_container.pack_start(self.item_code_entry, False, False, 10)
        entry_container.pack_start(item_name_label, False, False, 0)

        # Payment Mode Container
        payment_mode_container = Gtk.HBox(False, 10)
        payment_mode_label = Gtk.Label("Payment Mode: ")
        self.payment_mode_entry = Gtk.Entry()

        button1 = Gtk.RadioButton.new_with_label_from_widget(None, "Cash")
        button2 = Gtk.RadioButton.new_with_label_from_widget(button1, "Card")
        button3 = Gtk.RadioButton.new_with_label_from_widget(
            button1, "Online(PayTM/Tez)")
        button4 = Gtk.RadioButton.new_with_label_from_widget(button1, "Swiggy")
        button1.connect("toggled", self._on_button_toggled)
        button2.connect("toggled", self._on_button_toggled)
        button3.connect("toggled", self._on_button_toggled)
        button4.connect("toggled", self._on_button_toggled)

        payment_mode_container.pack_start(payment_mode_label, False, False, 0)
        payment_mode_container.pack_start(button1, False, False, 0)
        payment_mode_container.pack_start(button2, False, False, 0)
        payment_mode_container.pack_start(button3, False, False, 0)
        payment_mode_container.pack_start(button4, False, False, 0)
        self.pack_start(payment_mode_container, False, False, 10)

        # Date and Bill Number
        date_bill_container = Gtk.HBox(False, 10)
        self.pack_start(date_bill_container, False, False, 0)
        current_date = datetime.datetime.now()
        date_label = Gtk.Label()
        date_label.set_markup(
            "<b>Date: " + current_date.strftime("%d/%m/%Y") + "</b>")
        date_bill_container.pack_start(date_label, False, False, 5)
        bill_number = Gtk.Label()
        bill_number.set_markup("<b>Bill Number: </b>")
        self.bill_number_label = Gtk.Label(str(self.bill_number_fromdb))
        date_bill_container.pack_start(bill_number, False, False, 0)
        date_bill_container.pack_start(self.bill_number_label, False, False, 0)

        # Middle Container
        middle_vbox = Gtk.VBox(False, False, 0)
        self.pack_start(middle_vbox, False, False, 0)

        middle_box = Gtk.Box()
        middle_vbox.pack_start(middle_box, False, False, 0)
        middle_box.set_size_request(450, 200)
        self.bill_list_store = Gtk.ListStore(str, int, int, int)
        self.bill_tree_view = Gtk.TreeView(self.bill_list_store)
        for i, column_title in enumerate(["Food Item", "Price", "Quantity", "Total"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_min_width(200)
            self.bill_tree_view.append_column(column)
        middle_box.pack_start(self.bill_tree_view, False, False, 0)
        separator = Gtk.HSeparator()
        separator.set_size_request(4, 5)
        middle_vbox.pack_start(separator, False, False, 0)

        # Bottom Container
        bottom_box = Gtk.HBox(False, False, 0)
        self.pack_start(bottom_box, False, False, 0)
        clear_button = Gtk.Button("Clear")
        clear_button.connect("clicked", self._clear_bill)
        total_label = Gtk.Label("Total: ")

        self.total_Entry = Gtk.Label()
        self.total_Entry.set_markup(
            "<span font_desc='Arial 20'>{}</span>".format(str(0)))
        bottom_box.pack_start(clear_button, False, False, 0)
        bottom_box.pack_end(self.total_Entry, False, False, 0)
        bottom_box.pack_end(total_label, False, False, 80)

    def _key_pressed(self, widget, event):
        """
        Handles Key Pressed Event
        """
        key_value = event.keyval
        key_name = Gdk.keyval_name(key_value)
        key_mapping = {'equal': self._add_item_to_bill,
                       'Return': self._final_bill}

        if(key_name in key_mapping):
            key_mapping[key_name]()

    def _key_pressed_customer(self, widget, event):
        """
        Handles Key Pressed Event
        """
        key_value = event.keyval
        key_name = Gdk.keyval_name(key_value)
        key_mapping = {
            'Return': self._get_customer}

        if(key_name in key_mapping):
            key_mapping[key_name]()

    def _on_button_toggled(self, button):
        """
        Handles payment Mode toggle
        """
        if button.get_active():
            self.payment_mode = button.get_label()

    def show_items_popup(self, *args):
        self.popover.set_relative_to(args[0])
        self.popover.show_all()
        self.popover.popup()

    def _get_customer(self):
        db = DatabaseOperations()
        mobile_number = int(self.mobile_number_entry.get_text())
        db.get_customer_details(mobile_number)

    def _add_item_to_bill(self):
        """
        Add the item to the list
        """
        item_code = int(self.item_code_entry.get_text())
        self.item_code_entry.set_text("")
        global item_list_from_database
        food_item = item_list_from_database.get(int(item_code))
        if food_item == None:
            InformationDialog("Invalid Item Code", "Enter Valid Item Code")
        else:
            self.total_amount += food_item.item_price
            self.total_Entry.set_markup(
                "<span font_desc='Arial 20'>{}</span>".format(str(self.total_amount)))
            if item_code not in self.item_list_for_bill:
                temporary_item_for_bill = [
                    food_item.item_name, food_item.item_price, 1, food_item.item_price]
                self.item_list_for_bill.setdefault(
                    int(item_code), temporary_item_for_bill)
            else:
                item_from_bill = self.item_list_for_bill.get(item_code)
                item_from_bill[2] += 1
                item_from_bill[3] = item_from_bill[1] * item_from_bill[2]
                self.item_list_for_bill[item_code] = item_from_bill
        self.update_bill()

    def update_bill(self):
        """
        Updates the bill list
        """
        self.bill_list_store.clear()
        for column in self.bill_tree_view.get_columns():
            self.bill_tree_view.remove_column(column)
        for item_code in self.item_list_for_bill:
            self.bill_list_store.append(
                list(self.item_list_for_bill.get(int(item_code))))
        for i, column_title in enumerate(["Food Item", "Price", "Quantity", "Total"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_min_width(200)
            self.bill_tree_view.append_column(column)
        self.bill_tree_view.set_model(self.bill_list_store)

    def _final_bill(self):
        """
        Finalize the bill
        """
        db = DatabaseOperations()
        dialog_box = Gtk.Dialog("Print Bill", None, Gtk.DialogFlags.MODAL, (
            Gtk.STOCK_YES, 1, Gtk.STOCK_NO, 2, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        dialog_box.set_size_request(150, 100)
        box = dialog_box.get_content_area()
        box.add(Gtk.Label("Do you want to print the Bill?"))
        dialog_box.show_all()
        response = dialog_box.run()
        if response == 1:
            xlsUtility = XLSWriterUtility()
            xlsUtility.generate_bill(
                self.bill_number_fromdb, self.item_list_for_bill, self.total_amount)
            db.enter_bill_into_database(
                self.item_list_for_bill, self.total_amount, self.bill_number_fromdb, self.payment_mode)
            db.increment_bill_number() # Increment bill Number in database
            self.bill_number_fromdb = int(db.get_bill_number())
            self.bill_number_label.set_text(str(self.bill_number_fromdb))
            self._clear_bill()
        elif response == 2:
            db.enter_bill_into_database(
                self.item_list_for_bill, self.total_amount, self.bill_number_fromdb, self.payment_mode)
            db.increment_bill_number()
            self.bill_number_fromdb = int(db.get_bill_number())
            self.bill_number_label.set_text(str(self.bill_number_fromdb))
            self._clear_bill()
        elif response == Gtk.ResponseType.CANCEL:
            dialog_box.destroy()
        dialog_box.destroy()

    def _clear_bill(self, *args):
        """
        Clear all the variables related to the bill
        """
        self.bill_list_store.clear()
        self.item_list_for_bill.clear()
        self.total_amount = 0
        self.total_Entry.set_markup(
            "<span font_desc='Arial 20'>{}</span>".format(str(0)))

    def add_item_to_list(self, item):
        global item_list_from_database
        item_list_from_database[int(item[0])] = {
            'item_name': item[1], 'cost': int(item[2])}
