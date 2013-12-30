#!flask/bin/python
from flask import jsonify,make_response,request, render_template, abort
import forecastio, dbUtil
from app import app, models
from config import FORECASTIO_KEY


@app.route('/', methods = ['GET'])
def render_home():
    items = models.Todos.query.order_by(models.Todos.timestamp.desc()).all()
    return render_template("home.html", todos = items)

@app.route('/corkboard/api/v1/todos', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': tasks } )

@app.route('/corkboard/api/v1/todos/add/', methods = ['POST'])
def create_task():
    if ((request.json is None)):
        abort(400)
    data = [dict(message=request.json['message'], latitude='105', longitude='108')]
    statusMsg = dbUtil.insert_new_msg(data)
    if( statusMsg['status'] == "OK" ):
        result = dbUtil.get_latest_record()
        record = result['item'][0]

        recordDict = {
            'id': record.id,
            'timestamp': record.timestamp,
            'message': record.message,
            'latitude': record.latitude,
            'longitude': record.longitude
        }

        return make_response(jsonify( { 'status': statusMsg['status'], 'record': recordDict }), 201)
    else:
        return make_response(jsonify( { 'status': statusMsg['status'] } ), 400)


@app.route('/corkboard/api/v1/weather/<lat>/<lng>/', methods = ['GET'])
def get_weather(lat=None, lng=None):
    forecast = forecastio.load_forecast(FORECASTIO_KEY, lat, lng)
    currently = forecast.currently()
    dayInfo = {}
    for day in forecast.daily().data:
        dayInfo.update( generate_weather_dic( day ) )

    return make_response(jsonify(dict(current=generate_weather_dic(currently), daily=dayInfo, status='OK')), 201)


@app.route('/corkboard/api/v1/hello/')
@app.route('/corkboard/api/v1/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not Found' } ), 404)

@app.errorhandler(500)
def server_error(error):
        return make_response(jsonify( {'error': 'Server error'} ), 500)

def generate_weather_dic( object ):
    dayInfo = {}
    dateSt = None
    if not (object is None):
        
        try:
            dateSt = object.time.strftime("%m-%d-%Y")
        except Exception, e:
            dateSt = str(object.utime)

        dayInfo["data"] = {
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
    app.run(host = '0.0.0.0')