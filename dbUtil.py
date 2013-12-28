#!flask/bin/python
# -*- coding: utf-8 -*-
import time, json

def insert_new_msg( jsonData, mysql ):
	if not ( jsonData is None ):
		try:
			cur = mysql.get_db().cursor()
			data = json.loads(jsonData);

			cur.execute("INSERT INTO TO_DO(MESSAGE, LATITUDE, LONGITUDE) VALUES (%s, %s, %s)",
				( data[0]['message'] , data[0]['lat'], data[0]['lng']) )

			to_dos = {};
			cur.execute("select * from TO_DO TD ORDER BY TD.TIMESTAMP DESC");
			results = cur.fetchall();
			for row in results:
				itemId = row[0]; 
				item = {
					'id' : itemId,
					'timestamp' : str(row[1]),
					'message' : row[2],
					'lat'	: row[3],
					'lng'	: row[4]
				}

				to_dos[itemId] = item;

			return json.dumps([{
				'status' : 'OK',
				'data'	: to_dos
				}]);

		except Exception, e:
			raise e

	else:
		return make_response(jsonify( {
			'status' : 'error',
			'message' : 'Data provided is empty.'
		}), 404);

