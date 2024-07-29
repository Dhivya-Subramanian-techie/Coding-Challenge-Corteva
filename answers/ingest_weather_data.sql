-- -----------------------------------------------------------------------------------------------
-- Data Ingestion and Data Cleaning
-- -----------------------------------------------------------------------------------------------

-- Step 1: Create Logging Table
CREATE OR REPLACE TABLE ingest_log (
    id INT AUTOINCREMENT PRIMARY KEY,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    records_ingested INT
);

-- Describe the ingest_log table (for verification)
DESCRIBE TABLE ingest_log;

-- Step 2: Create Stage for Raw Data
CREATE OR REPLACE STAGE STG_weather;
-- Show the files in the stage (for verification)
-- Uncomment the following line after uploading files
-- LIST @STG_weather;

-- Step 3: Create a File Format (if needed)
-- Adjust the file format parameters according to your file type
CREATE OR REPLACE FILE FORMAT csv_format
TYPE = 'CSV'
FIELD_DELIMITER = '\t'
COMPRESSION = 'GZIP';

-- Step 4: Create procedure for ingesting data from Stage into staging_weather_data Table
CREATE OR REPLACE PROCEDURE ingest_weather_data()
RETURNS STRING
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS
$$

    var start_time = Date.now();
    var rows_before = 0;
    var rows_after = 0;
    var rows_inserted = 0;

    try {
            -- Count rows before the merge
            var count_before_command = `SELECT COUNT(*) AS count_before FROM staging_weather_data`; 
            var count_before_result = snowflake.execute({sqlText: count_before_command});
            rows_before = count_before_result.next() ? count_before_result.getColumnValue(1) : 0;

            -- Merge data from stage into the table
            var sql_command = `
            MERGE INTO staging_weather_data t
            USING (
                SELECT 
                    $1::DATE AS record_date,
                    CASE
                        WHEN $2 = '-9999' THEN NULL
                        ELSE ($2::DECIMAL(5,1) / 10)
                    END AS wx_max_temp,
                    CASE
                        WHEN $3 = '-9999' THEN NULL
                        ELSE ($3::DECIMAL(5,1) / 10)
                    END AS wx_min_temp,
                    CASE
                        WHEN $4 = '-9999' THEN NULL
                        ELSE ($4::DECIMAL(5,1) / 10)
                    END AS wx_precipitation,
                    SPLIT_PART(SPLIT_PART(METADATA$FILENAME, '/', -1), '.', 1) AS wx_stationid
                FROM @STG_weather (FILE_FORMAT => 'csv_format')
            ) s 
            ON t.wx_date = s.record_date AND t.wx_stationid = s.wx_stationid
            WHEN NOT MATCHED THEN
                INSERT (wx_date, wx_max_temp, wx_min_temp, wx_precipitation, wx_stationid)
                VALUES (s.record_date, s.wx_max_temp, s.wx_min_temp, s.wx_precipitation, s.wx_stationid)
        `;
        snowflake.execute({sqlText: sql_command});

        
        -- Count rows after the merge
        var count_after_command = `SELECT COUNT(*) AS count_after FROM staging_weather_data`;
        var count_after_result = snowflake.execute({sqlText: count_after_command});
        rows_after = count_after_result.next() ? count_after_result.getColumnValue(1) : 0;

        -- Calculate rows inserted
        rows_inserted = rows_after - rows_before;

        -- Log the ingestion process
        var end_time = Date.now();
        var log_command = `
            INSERT INTO ingest_log (start_time, end_time, records_ingested)
            VALUES (TO_TIMESTAMP('${(start_time)}'), TO_TIMESTAMP('${(end_time)}'), ${rows_inserted})
        `;

        snowflake.execute({sqlText: log_command});

        return 'Data ingestion completed successfully. Records ingested: ' + rows_inserted;

    } catch (err) {
        return 'Error: ' + err.message;
    }
$$;

-- Step 5: Use SnowSQL or Snowflake’s web interface to execute the script.
    -- Step 5.1: snowsql -a <account> -u <user> -w <warehouse> -d <database> -s <schema> 
    -- Step 5.2: PUT file://E:/GitHub_Local/Coding-Challenge-corteva/wx_data/* @STG_weather;

 -- Step 6: Ingest Data from Stage to Table
CALL ingest_weather_data();