#!flask/bin/python
import datetime, forecastio


FORECASTIO_KEY = '5481d13c75c7b5a7f56411647a4e88df'
forecast = forecastio.load_forecast(FORECASTIO_KEY, '41.4804806', '-81.9783582', None, "us")
time = int(1387256400);
dTime = datetime.datetime.fromtimestamp(time)

for day in forecast.daily().data:
	for attr in dir(day):
		print "day.%s = %s" % (attr, getattr(day, attr))