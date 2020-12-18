import os

def generate_order_id():
	return os.urandom(3).hex()

