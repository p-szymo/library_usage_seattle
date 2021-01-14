from datetime import datetime


def timestamp():
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	return current_time


def status_update(msg):
	print('Current time =', timestamp())
	print('-------------------------------')
	print(msg)
	print('')