from flask import (
	# Creating app instances
	Flask,
	# Rendering Jinja2 templates
	render_template )
	
import traceback
import pprint

class errorhandler:
	def __init__(self):
		pass

        def setlogger(self, logger):
                pass
                self.logger = logger
	
	def handleError(self, message):
		print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		print "Encountered Error"
		print message
		
		self.logger.error(message)
		self.logger.handlers[0].flush()
		
		return render_template('errors/error.html', ERROR_MESSAGE = message)
		
	def rethrowException(self, exc):
		message = "An exception occurred:\n"
	 	message += str(exc)	 
	 	message += traceback.format_exc()
	 	
	 	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		print "Encountered Exception"
		print message
	 	
		self.logger.exception('Exception:'+str(exc), exc_info=True)
		
		#pprint.pprint(self.logger.handlers)
		
		self.logger.handlers[0].flush()
		raise
		
	def handleException(self, exc):
		self.logger.exception('Exception:'+str(exc), exc_info=True)
		self.logger.handlers[0].flush()
	
		message = "An exception occurred:\n"
	 	message += str(exc)	 
	 	message += traceback.format_exc()
	 	
	 	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		print "Encountered Exception"
		print message
	 	
		return render_template('errors/error.html', ERROR_MESSAGE = message)
