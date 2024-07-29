----Create the new table structure for storing the results.
 CREATE OR REPLACE TABLE weather_statistics (
    ws_year INT,            -- Year of the observation
    ws_stationid STRING,    -- Weather station ID
    ws_avg_max_temp FLOAT,  -- Average maximum temperature (in degrees Celsius)
    ws_avg_min_temp FLOAT,  -- Average minimum temperature (in degrees Celsius)
    ws_total_precipitation FLOAT,  -- Total accumulated precipitation (in centimeters)
    PRIMARY KEY (ws_year, ws_stationid)
);

-------Insert the calculated values into the new table

INSERT INTO weather_statistics (ws_year, ws_stationid, ws_avg_max_temp, ws_avg_min_temp, ws_total_precipitation)
WITH weather_data AS (
    SELECT 
        YEAR(wx_date) AS year,
        wx_stationid,
        CASE WHEN wx_max_temp IS NOT NULL THEN wx_max_temp ELSE NULL END AS max_temp_celsius,
        CASE WHEN wx_min_temp IS NOT NULL THEN wx_min_temp ELSE NULL END AS min_temp_celsius,
        CASE WHEN wx_precipitation IS NOT NULL THEN wx_precipitation ELSE NULL END AS precipitation_cm
    FROM staging_weather_data
)
SELECT 
    year,
    wx_stationid,
    ROUND(AVG(max_temp_celsius), 1) AS avg_max_temp,
    ROUND(AVG(min_temp_celsius), 1) AS avg_min_temp,
    ROUND(SUM(precipitation_cm), 1) AS total_precipitation
FROM weather_data
GROUP BY year, wx_stationid
ORDER BY year, wx_stationid;
