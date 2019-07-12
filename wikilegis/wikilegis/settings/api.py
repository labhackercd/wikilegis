from decouple import config


API_KEY = config('API_KEY', default='apikey')
TASTYPIE_DEFAULT_FORMATS = ['json']