{{ config(alias='calendar',
enabled=false) }}

WITH 
dategen AS (
    SELECT DATEADD(DAY, SEQ4(), '2021-01-01')::DATE AS dt
    FROM TABLE(GENERATOR(ROWCOUNT=>2000))
)
SELECT
    dategen.dt AS id,
    -- date
    TO_CHAR(dategen.dt,'yyyy-mm-dd')::char(10) AS date_text_iso,
    TO_CHAR(dategen.dt,'yyyymmdd')::int AS date_num,
    TO_CHAR(dategen.dt,'DD-MON-YY')::char(9) AS date_text_alt,
    TO_CHAR(dategen.dt,'DD/MM/YYYY')::char(10) AS date_text_us,
    -- day of week
    DAYOFWEEK(dategen.dt) AS day_no_of_week,
    DAYNAME(dategen.dt) AS day_of_week_name_short,
    DECODE(DAYNAME(dategen.dt),
    'Mon','Monday','Tue','Tuesday',
    'Wed','Wednesday','Thu','Thursday',
    'Fri','Friday','Sat','Saturday',
          'Sun','Sunday') AS DAY_OF_WEEK_NAME,
    IFF(DAYOFWEEK(dategen.dt) IN (0,6),1,0)::BOOLEAN AS is_weekend,
    NOT is_weekend AS is_weekday,
    CASE WHEN is_weekend = True then 'Weekend' else 'Weekday' end as weekday_type_name,
    -- week
    EXTRACT(weekiso FROM dategen.dt) AS week_no_of_year,
    CONCAT(TO_CHAR(dategen.dt,'YYYY"-W'), LPAD(week_no_of_year,2,'0')) AS calendar_week,
    last_day(dategen.dt,'WEEK') as week_date_sunday,
    last_day(dategen.dt,'WEEK')-1 as week_date_saturday,
    --DATE_TRUNC('week',dategen.dt::date)::date + 5 AS week_end_date,
    dategen.dt + (6-DAYOFWEEK(dategen.dt)) as fiscal_period,
    -- month
    EXTRACT(MONTH FROM dategen.dt) AS month_no_of_year,
    EXTRACT(DAY FROM dategen.dt) AS day_of_month,
    TO_CHAR(dategen.dt,'MMMM')::VARCHAR(9) AS month_name,
    TO_CHAR(dategen.dt,'MON')::CHAR(3) AS month_name_short,
    CONCAT(TO_CHAR(dategen.dt,'yyyy-'),'M',TO_CHAR(dategen.dt,'MM')) AS year_month,
    CONCAT(TO_CHAR(dategen.dt,'yy'),'-', TO_CHAR(dategen.dt,'MM')) AS year_month_short,
    TO_CHAR(dategen.dt,'yyyy-MM MMMM') AS year_month_long,
    -- quarter
    EXTRACT(QUARTER FROM dategen.dt) AS quarter_no_of_year,
    CONCAT('Q',LTRIM(TO_CHAR(quarter_no_of_year,'0'),TO_CHAR(dategen.dt,'yy')))::CHAR(7) AS quarter,
    CONCAT('Quarter ',quarter_no_of_year) AS quarter_of_year_name,
    CONCAT('Q',quarter_no_of_year) AS quarter_of_year_short,
    CONCAT(TO_CHAR(dategen.dt,'yyyy-'),'Q',LTRIM(TO_CHAR(quarter_no_of_year,'0')))::CHAR(7) AS year_quarter,
    CONCAT(LTRIM(TO_CHAR(quarter_no_of_year,'0')), 'Q', TO_CHAR(dategen.dt,'yy'))::CHAR(4) AS year_quarter_short,
    dategen.dt - (DATE_TRUNC('QUARTER',dategen.dt)::DATE) + 1 AS day_of_quarter_no,
    -- phase
    CASE WHEN quarter_no_of_year <=2 THEN 1 ELSE 2 END AS phase_no_of_year,
    CONCAT('P',LTRIM(TO_CHAR(phase_no_of_year,'0'),TO_CHAR(dategen.dt,'yy')))::CHAR(7) AS phase,
    CONCAT('Phase ',phase_no_of_year) AS phase_of_year_name,
    CONCAT('P',phase_no_of_year) AS phase_of_year_short,
    CONCAT(TO_CHAR(dategen.dt,'yyyy-'),'P',TO_CHAR(phase_no_of_year))::CHAR(7) AS year_phase,
    CONCAT(TO_CHAR(phase_no_of_year), 'P', TO_CHAR(dategen.dt,'yy'))::CHAR(4) AS year_phase_short,
    -- year
    YEAR(dategen.dt) AS year,
    CONCAT('CY ',YEAR(dategen.dt))::CHAR(7) AS year_name,
    EXTRACT(DOY FROM dategen.dt) AS day_of_year
FROM dategen