from flask_babel import Babel
print([attr for attr in dir(Babel) if 'locale' in attr])