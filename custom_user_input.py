'''
@Author: Rene Jacques
March 17, 2019
'''

class Custom_User_Input:
	'''Custom user input class used to streamline querying and inpurt error checking'''
	def __init__(self):
		self.queries = {}

	def get_input(self):
		'''Get all of the processed queries'''
		if not self.queries:
			print('QUERIES IS EMPTY')
		else:
			return self.queries

	def query(self,text,variable,isNumber=False,limitLength=False,limit=-1,exactLength=False,length=-1,noCharacters=False,charList=None,cSepNum=False):
		'''Create a new query with parameters:
			
			text = text displayed to the user
			variable = dictionary key for input storage
			isNumber = set this flag if the input is only a number
			limitLength = set this flag if the input has a length limit
			limit = set this value if the limitLength flag is true to set the length limit
			exactLength = set this flag if the input has an exact length
			length = set this value if the exactLength is true to set the exact length
			noCharacters = set this flag if there are specific characters that are not allowed
			charList = the input of characters that are not allowed if the noCharacters flag is true
			cSepNum = set this flag if the input is comma separated numbers
		'''
		q_in = input(text) # get input

		# check if input is a number
		if isNumber:
			try:
				q_in = float(q_in)
			except:
				print('Invalid Input: Not a Number')
				return False

		# check if input length is valid
		if limitLength:
			if len(q_in) > limit:
				print('Invalid Input: Input is too long')
				return False

		# check if input length is valid
		elif exactLength:
			if len(q_in) != length:
				print('Invalid Input: Input is not the correct length')
				return False

		# check if characters in charList are in input
		if noCharacters and not isNumber:
			for char in q_in:
				if char in charList:
					print('Invalid Input: '+char+' found in input')
					return False

		# check if input is comma separated 
		if cSepNum:
			for char in q_in:
				if char in '!@#$%^&*()_+-=[]\{\}|`~/.<>?;:':
					print('Invalid Input: '+char+' is not a number')
					return False

			words = q_in.split(',')
			
			numbers = []
			for w in words:
				numbers.append(int(w))
			q_in = numbers

		self.queries[variable] = q_in

def test():
	c = Custom_User_Input()
	c.query('What is your name? ','name')
	c.query('How old are you? ','age',isNumber=True)
	c.query('What is your favorite color? ','color')
	print(c.get_input())

if __name__ == '__main__':
	test()