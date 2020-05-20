
def check(x):
	try:
		return type(eval(x))
	except:
		return type(x)