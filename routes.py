#!flask/bin/python
from flask import Flask, jsonify,make_response,request, render_template,json
from flask.ext.mysql import MySQL
import forecastio, datetime, dbUtil

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object('config')

mysql = MySQL();
mysql.init_app(app)

FORECASTIO_KEY = '5481d13c75c7b5a7f56411647a4e88df'

@app.route('/info-deck', methods = ['GET'])
def render_home():
    return render_template('home.html')


@app.route('/info-deck/api/v1/todos', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': tasks } )

@app.route('/info-deck/api/v1/todos', methods = ['POST'])
def create_task():
    #if not request.json or not 'message' in request.json:
        #abort(400)
    data = [{
        'message'   :   'this is a test!',
        'lat'   :   '105',
        'lng'   :   '108'
    }];
    jsonData = json.dumps(data);
    dbUtil.insert_new_msg(jsonData, mysql);
    return make_response(jsonify( { 'status': 'OK' } ), 201)

@app.route('/info-deck/api/v1/weather/<lat>/<lng>/', methods = ['GET'])
def get_weather(lat=None, lng=None):
    forecast = forecastio.load_forecast(FORECASTIO_KEY, lat, lng)
    currently = forecast.currently()
    dayInfo = {}
    for day in forecast.daily().data:
        dayInfo.update( generateWeatherDic( day ) )

    return make_response(jsonify( {
        #order json properties alphabetically just to make things easier
        'current': generateWeatherDic( currently ), 
        'daily'  : dayInfo,
        'status' : 'OK', 
        'units'  : forecast.units,
        } ), 201)


@app.route('/info-deck/api/v1/hello/')
@app.route('/info-deck/api/v1/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.errorhandler(500)
def server_error(error):
        return make_response(jsonify( {'error': 'Server error'} ), 500)

def generateWeatherDic( object ):
    dayInfo = {}
    dateSt = None
    if not (object is None):
        
        try:
            dateSt = object.time.strftime("%m-%d-%Y")
        except Exception, e:
            dateSt = str(object.utime)

        dayInfo[str(object.utime)] = {
        #order json properties alphabetically just to make things easier
                'date' : dateSt,
                'high' : object.temperatureMax,
                'icon' : object.icon,
                'low' : object.temperatureMin,
                'precipAccum' : str(object.precipAccumulation),
                'precipProbability' : formatFloatingPoint(object.precipProbability , 100),
                'precipType' : object.precipType,
                'summary' : object.summary,
                'windSpeed' : object.windspeed
            }
        return dayInfo

def formatFloatingPoint( val, multiplier = None ):
    if not ( val is None ):
        if not ( multiplier is None ):
            return ( "%0.2f" % (val * multiplier) )
        else:
            return ( "%0.2f" % (val) )

if __name__ == '__main__':
    app.run(
        debug = True,
        host='0.0.0.0')
    