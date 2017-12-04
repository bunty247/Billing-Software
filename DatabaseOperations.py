from pymongo import MongoClient
import datetime
from collections import Counter

class DatabaseOperations:

	def __init__(self):
		""" 
		Module for all the database operations.
		"""
		client = MongoClient("localhost", 27017)
		self.db = client['Billing']

	def get_all_items(self):
		""" 
		Returns a dictionary of all the items on init
		"""
		food_items_dict = {}
		food_items_from_db = self.db.food_items.find()
		for food_item in food_items_from_db:
			food_items_dict.setdefault(int(food_item['item_code']) , {'item_name' : food_item['item_name'], 
				'cost' : int(food_item['cost'])})
		return food_items_dict

	def get_bill_number(self):
		""" 
		Returns the current bill number from the database
		"""
		return self.db.sequence.find_one({'id' : 'bill_number'}).get('current_bill_number')

	def enter_bill_into_database(self, item_list_for_bill, total):
		""" 
		Returns the current bill number from the database
		"""
		current_date = datetime.datetime.now().strftime("%d/%m/%Y")
		item_count = self.db.daily_record.find_one({'date' : str(current_date)}).get('item_count')
		current_total = int(self.db.daily_record.find_one({'date' : str(current_date)}).get('daily_total'))
		updated_total = current_total + total	
		new_count = {item[0]: item[2] for code, item in item_list_for_bill.items()}
		updated_count = dict(Counter(item_count) + Counter(new_count))
		self.db.daily_record.update({'date' : str(current_date)}, { '$set' : {'item_count' : updated_count, 
			'daily_total' : updated_total}})

	def get_and_update_bill_number_on_init(self):
		""" 
		Get/Update bill number on init
		Return:
			Returns the bill number from the database on application
		"""
		bill_date = self.db.sequence.find_one({'id' : 'bill_number'}).get('date')
		current_date = datetime.datetime.now().strftime("%d/%m/%Y")
		if(bill_date < current_date):
			self.db.sequence.update({'id' : 'bill_number'}, {'$set' : {'date' : str(current_date), 
				'current_bill_number' : 1}})
		return self.db.sequence.find_one({'id' : 'bill_number'}).get('current_bill_number')

	def increment_bill_number(self):
		""" 
		Increment bill number in the database
		"""
		self.db.sequence.update({'id' : 'bill_number'}, {'$inc' : {'current_bill_number' : 1}})

	def create_daily_record_entry(self):
		current_date = datetime.datetime.now().strftime("%d/%m/%Y")
		result = self.db.daily_record.find({'date': str(current_date)}).count()
		if result == 0:
			self.db.daily_record.insert({'date' : str(current_date), 'item_count' : {}, 'daily_total' : 0})

	def get_records(self, start_date, end_date):
		""" 
		Return all records from the database
		Args:
			param1(str):Start Date
			param1(str):End Date
		Return:
			Returns a dictionary of the records
		"""
		result = self.db.daily_record.find({'date' : {'$gte' : start_date, '$lte' : end_date}})
		records_dict = {}
		for record in result:
			records_dict.setdefault(record.get('date'), [int(record.get('daily_total')), record.get('item_count')])
		return records_dict

	def add_new_item(self, item):
		""" 
		Inserts new item in the database
		Args:
			param1(list):List of item detils
		"""
		self.db.food_items.insert({"item_code" : item[0], "item_name" : item[1], "cost" : item[2]})

	def edit_item(self, item):
		""" 
		Edit existing item in the database
		Args:
			param1(list):List of item detils
		"""
		self.db.food_items.update({"item_code" : item[0]}, {'$set' : {"item_name" : item[1], "cost" : item[2]}})
