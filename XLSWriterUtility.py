import xlsxwriter
import datetime

class XLSWriterUtility:

	def generate_bill(self, bill_number, item_list_for_bill, total):
		"""
		Generate a .xlsx File of the bill
			Args:
				param1 (str): Bill number
				param2 (list): List of items in the bill
				param2 (str): Total of the bill
		"""

		workbook = xlsxwriter.Workbook('bill.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.set_margins(0, 0, 0, 0)
		worksheet.set_column('A:A', 15)
		worksheet.set_column('B:B', 4)
		worksheet.set_column('C:C', 4)
		worksheet.set_column('D:D', 11)
		merge_format = workbook.add_format({
		'bold': 1,
		'border': 0,
		'align': 'center',
		'valign': 'vcenter'})
		border_format = workbook.add_format({'border' : 3,'left' : 0, 'right' : 0})
		total_format = workbook.add_format({'border' : 3,'left' : 0, 'right' : 0, 'font_size' : 15, 'bold' : 1})
		worksheet.merge_range('A1:D1', "Chandan Snacks Center", merge_format)
		worksheet.merge_range('A2:D2', "Shop No.4A, Satyasgar CHS,", merge_format)
		worksheet.merge_range('A3:D3', "Sector - 4, Kalamboli.", merge_format)
		worksheet.merge_range('A4:B4', "Date: " + datetime.datetime.now().strftime("%d-%m-%Y"), merge_format)
		worksheet.merge_range('C4:D4', "Bill Number: " + str(bill_number) , merge_format)
		worksheet.write(4, 0, "Particulars", border_format)
		worksheet.write(4, 1, "Qty.", border_format)
		worksheet.write(4, 2, "Rate", border_format)
		worksheet.write(4, 3, "Amount", border_format)

		row = 5
		column = 0
		for item_code, food_item in item_list_for_bill.items():
			worksheet.write(row, column, food_item[0])
			worksheet.write(row, column + 1, food_item[2])
			worksheet.write(row, column + 2, food_item[1])
			worksheet.write(row, column + 3, food_item[3])
			row += 1

		worksheet.write(row, 0, "Total", total_format)
		worksheet.write(row, 1, "", border_format)
		worksheet.write(row, 2, "", border_format)
		worksheet.write(row, 3, total, total_format)
		worksheet.set_row(row, 15)
		row += 1
		worksheet.write(row, 0, "Thank You!")
		worksheet.write(row, 2, "Visit Again☺")
