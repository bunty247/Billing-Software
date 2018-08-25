class BillingSoftwareUtility(object):

    def insert_only_number(self, *args):
		#print(args)
        """
		Appends only 0-9 numbers in the input box
		"""
        text = args[0].get_text().strip()
        args[0].set_text(''.join([i for i in text if i in '0123456789']))
