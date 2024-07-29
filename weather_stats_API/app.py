from flask import Flask, request, jsonify
import snowflake.connector
from flask_restx import Api, Resource, fields
import config

app = Flask(__name__)

# Configure Snowflake connection using config file
app.config['SNOWFLAKE_USER'] = config.SNOWFLAKE_USER
app.config['SNOWFLAKE_PASSWORD'] = config.SNOWFLAKE_PASSWORD
app.config['SNOWFLAKE_ACCOUNT'] = config.SNOWFLAKE_ACCOUNT
app.config['SNOWFLAKE_DATABASE'] = config.SNOWFLAKE_DATABASE
app.config['SNOWFLAKE_SCHEMA'] = config.SNOWFLAKE_SCHEMA

def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user=app.config['SNOWFLAKE_USER'],
        password=app.config['SNOWFLAKE_PASSWORD'],
        account=app.config['SNOWFLAKE_ACCOUNT'],
        database=app.config['SNOWFLAKE_DATABASE'],
        schema=app.config['SNOWFLAKE_SCHEMA']
    )
    return conn

api = Api(app, version='1.0', title='Weather API', description='A simple Weather API')

ns = api.namespace('api/weather', description='Weather operations')

weather_model = api.model('Weather', {
    'wx_id': fields.Integer(description='Weather ID'),
    'wx_date': fields.Date(description='Date'),
    'wx_max_temp': fields.Float(description='Maximum Temperature (tenths of a degree Celsius)'),
    'wx_min_temp': fields.Float(description='Minimum Temperature (tenths of a degree Celsius)'),
    'wx_precipitation': fields.Float(description='Precipitation (tenths of a millimeter)'),
    'wx_stationid': fields.String(description='Station ID')
})

stats_model = api.model('WeatherStats', {
    'ws_year': fields.Integer(description='Year'),
    'ws_stationid': fields.String(description='Station ID'),
    'ws_avg_max_temp': fields.Float(description='Average Maximum Temperature (in degrees Celsius)'),
    'ws_avg_min_temp': fields.Float(description='Average Minimum Temperature (in degrees Celsius)'),
    'ws_total_precipitation': fields.Float(description='Total Precipitation (in centimeters)')
})

@ns.route('/')
class WeatherList(Resource):
    @ns.doc('list_weather')
    @ns.doc(params={
        'date': 'Filter results by date (YYYY-MM-DD)',
        'station_id': 'Filter results by station ID',
        'page': 'Page number for pagination',
        'per_page': 'Number of records per page'
    })
    @ns.marshal_list_with(weather_model)
    def get(self):
        """List weather data"""
        date = request.args.get('date')
        station_id = request.args.get('station_id')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        query = "SELECT wx_id, wx_date, wx_max_temp, wx_min_temp, wx_precipitation, wx_stationid FROM staging_weather_data WHERE 1=1"
        
        if date:
            query += f" AND wx_date = '{date}'"
        
        if station_id:
            query += f" AND wx_stationid = '{station_id}'"
        
        offset = (page - 1) * per_page
        query += f" LIMIT {per_page} OFFSET {offset}"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0].lower() for desc in cursor.description]  # Convert column names to lowercase
        cursor.close()
        conn.close()
        
        result = [dict(zip(columns, row)) for row in rows]
        
        # Debugging statement
        print("Weather Data Result: ", result)
        
        return result

@ns.route('/stats')
class WeatherStats(Resource):
    @ns.doc('get_weather_stats')
    @ns.doc(params={
        'date': 'Filter results by date (YYYY-MM-DD). The year is extracted from this date.',
        'station_id': 'Filter results by station ID',
        'page': 'Page number for pagination',
        'per_page': 'Number of records per page'
    })
    @ns.marshal_list_with(stats_model)
    def get(self):
        """Get weather statistics"""
        date = request.args.get('date')
        station_id = request.args.get('station_id')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                ws_year,
                ws_stationid,
                ws_avg_max_temp,
                ws_avg_min_temp,
                ws_total_precipitation
            FROM weather_statistics
            WHERE 1=1
        """
        
        if date:
            year = date[:4]  # Assuming date is in YYYY-MM-DD format
            query += f" AND ws_year = {year}"
        
        if station_id:
            query += f" AND ws_stationid = '{station_id}'"
        
        offset = (page - 1) * per_page
        query += f" LIMIT {per_page} OFFSET {offset}"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0].lower() for desc in cursor.description]  # Convert column names to lowercase
        cursor.close()
        conn.close()
        
        result = [dict(zip(columns, row)) for row in rows]
        
        # Debugging statement
        print("Weather Stats Result: ", result)
        
        return result

if __name__ == '__main__':
    app.run(debug=True)