-- Use the appropriate database and schema
USE DATABASE CORVETA_AGRI;
USE SCHEMA WEATHER;

-- Create the warehouse if not already created
CREATE WAREHOUSE LOAD_WH;

-- Create the staging_weather_data table
CREATE OR REPLACE TABLE staging_weather_data (
    wx_id INT AUTOINCREMENT PRIMARY KEY,        -- Unique identifier for each weather data record
    wx_date DATE NOT NULL,                      -- Date of the weather observation(YYYY-MM-DD format)
    wx_max_temp FLOAT,                          -- Maximum temperature recorded (in degrees Celsius)
    wx_min_temp FLOAT,                          -- Minimum temperature recorded (in degrees Celsius)
    wx_precipitation FLOAT,                     -- Amount of precipitation recorded (in centimeters)
    wx_stationid STRING NOT NULL,               -- Identifier for the weather station
    UNIQUE(wx_date, wx_stationid)               -- Unique constraint to ensure no duplicate records
);

-- Show the schema of the weather_data table
DESCRIBE TABLE weather_data;