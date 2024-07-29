# Code Challenge - Weather Stats API

This project offers a RESTful API to access weather data and stats, built with Flask and Flask-RESTx, and using Snowflake for data storage. Check out the answers to the code challenge in `answers/detailed_soln.docx`.

## Features

- Retrieve weather data filtered by date and station ID.
- Retrieve weather statistics filtered by year and station ID.
- Paginated responses for large datasets.
- Structured logging.
- Configurable settings through a config file.

## Project Structure

```bash
/weather_stats_API
│
├── config.py          # Snowflake connection settings
├── app.py             # Main Flask application file containing API endpoints
├── unit_tests.py      # Unit tests for testing the application
└── requirements.txt   # List of Python dependencies required for the application
```

## Prerequisites

- Snowflake Account: Ensure you have access to a Snowflake account.
- SnowSQL Client: Install SnowSQL for command-line operations.
- Raw Data Files: Have the raw weather data files ready for upload.


## Setup Instructions

### Clone repo

	git clone https://github.com/

	cd weather_stats_API

### Create a Virtual Environment (Recommended): 
    ### Creating a virtual environment ensures that your project's dependencies are managed separately from your system-wide Python installation.
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`

### Install Dependencies:
    pip install -r requirements.txt

### Update config.py file:
    SNOWFLAKE_USER = 'your_snowflake_user'
    SNOWFLAKE_PASSWORD = 'your_snowflake_pwd'
    SNOWFLAKE_ACCOUNT = 'your_snowflake_account'    #Example: 'abc1234.us-east-2.aws'
    SNOWFLAKE_DATABASE = 'your_snowflake_database'  #Example: 'CORVETA_AGRI'
    SNOWFLAKE_SCHEMA = 'your_snowflake_schema'      #Example: 'WEATHER'

## Execute SQL files in Snowflake
    - Extract the sql files from /answers folder and run them in Snowflake
    /answers
    ├── create_weather_data_table.sql   # [Problem 1] DDL Statements to create staging_weather_data table 
    ├── create_weather_data.sql         # [Problem 2] DDL Statements to data cleaning and ingestion
    ├── create_weather_stats.sql        # [Problem 3] DDL Statements to create weather_statistics table and calculate weather statistics

## Run weather_stats_API application
    python weather_stats_API/app.py     # [Problem 4] Main Flask application file containing API endpoints
### Endpoints
    The API provides the following endpoints:

    /api/weather: Retrieve weather data.
    /api/weather/stats: Retrieve weather statistics.
### Get Weather Data
    URL: /api/weather/
    Method: GET
    Query Parameters:
    date (optional): Filter by date (YYYY-MM-DD).
    station_id (optional): Filter by weather station ID.
    page (optional): Page number for pagination (default is 1).
    per_page (optional): Number of records per page (default is 10).
    Purpose:
    This endpoint retrieves weather data, optionally filtered by date and station ID. It supports pagination to handle large datasets efficiently.
### Get Weather Statistics
    URL: /api/weather/stats/
    Method: GET
    Query Parameters:
    date (optional): Filter results by date (YYYY-MM-DD). The year is extracted from this date for filtering.
    station_id (optional): Filter by weather station ID.
    page (optional): Page number for pagination (default is 1).
    per_page (optional): Number of records per page (default is 10).
    Purpose:
    This endpoint retrieves weather statistics, optionally filtered by year (extracted from the date parameter) and station ID. It also supports pagination to manage large datasets effectively.