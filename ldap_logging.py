import logging

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) # or whatever
handler = logging.FileHandler('test.txt', 'w', 'utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(name)s %(message)s')) # or whatever
root_logger.addHandler(handler)




