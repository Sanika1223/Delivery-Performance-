
CREATE TABLE delivery_stage2_import (
    delivery_id TEXT,
    delivery_partner TEXT,
    package_type TEXT,
    vehicle_type TEXT,
    delivery_mode TEXT,
    region TEXT,
    weather_condition TEXT,
    distance_km TEXT,
    package_weight_kg TEXT,
    delivery_time_hours TEXT,
    expected_time_hours TEXT,
    delayed TEXT,
    delivery_status TEXT,
    delivery_rating TEXT,
    delivery_cost TEXT,
    delivery_id_original TEXT,
    delivery_record_id TEXT,                  
    delivery_time_hours_original TEXT,
    expected_time_hours_original TEXT,
    time_data_quality TEXT
);


SELECT COUNT(*) AS total_records
FROM delivery_stage2_import;


SELECT *
FROM delivery_stage2_import
LIMIT 5;


CREATE TABLE IF NOT EXISTS delivery_analysis (
    delivery_record_id TEXT PRIMARY KEY,
    delivery_id_original TEXT,
    delivery_partner TEXT,
    package_type TEXT,
    vehicle_type TEXT,
    delivery_mode TEXT,
    region TEXT,
    weather_condition TEXT,
    distance_km NUMERIC,
    package_weight_kg NUMERIC,
    delivery_rating NUMERIC,
    delivery_cost NUMERIC,
    delayed TEXT,
    delivery_status TEXT,
    delivery_time_hours NUMERIC,
    expected_time_hours NUMERIC,
    delivery_time_hours_original TEXT,
    expected_time_hours_original TEXT,
    time_data_quality TEXT
);


SELECT COUNT(*)
FROM delivery_analysis;


SELECT *
FROM delivery_analysis
LIMIT 5;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'delivery_analysis'
ORDER BY ordinal_position;


INSERT INTO delivery_analysis (
    delivery_record_id,
    delivery_id_original,
    delivery_partner,
    package_type,
    vehicle_type,
    delivery_mode,
    region,
    weather_condition,
    distance_km,
    package_weight_kg,
    delivery_rating,
    delivery_cost,
    delayed,
    delivery_status,
    delivery_time_hours,
    expected_time_hours,
    delivery_time_hours_original,
    expected_time_hours_original,
    time_data_quality
)
SELECT
    delivery_record_id,
    delivery_id_original,
    delivery_partner,
    package_type,
    vehicle_type,
    delivery_mode,
    region,
    weather_condition,
    NULLIF(TRIM(distance_km), '')::NUMERIC,
    NULLIF(TRIM(package_weight_kg), '')::NUMERIC,
    NULLIF(TRIM(delivery_rating), '')::NUMERIC,
    NULLIF(TRIM(delivery_cost), '')::NUMERIC,
    delayed,
    delivery_status,
    NULL::NUMERIC,
    NULL::NUMERIC,
    delivery_time_hours_original,
    expected_time_hours_original,
    time_data_quality
FROM delivery_stage2_import
ON CONFLICT (delivery_record_id) DO NOTHING;


SELECT COUNT(*)
FROM delivery_analysis;


SELECT
    COUNT(*) AS total_deliveries
FROM delivery_analysis;


SELECT
    delivery_status,
    COUNT(*) AS total_deliveries,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM delivery_analysis
GROUP BY delivery_status
ORDER BY total_deliveries DESC;


SELECT
    delivery_partner,
    COUNT(*) AS total_deliveries,
    ROUND(AVG(delivery_cost), 2) AS average_delivery_cost,
    ROUND(AVG(delivery_rating), 2) AS average_rating
FROM delivery_analysis
GROUP BY delivery_partner
ORDER BY total_deliveries DESC;


SELECT
    region,
    COUNT(*) AS total_deliveries,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delivered'
    ) AS delivered,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delayed'
    ) AS delayed,

    COUNT(*) FILTER (
        WHERE delivery_status = 'failed'
    ) AS failed,

    ROUND(AVG(delivery_cost), 2) AS average_delivery_cost,

    ROUND(AVG(delivery_rating), 2) AS average_rating

FROM delivery_analysis
GROUP BY region
ORDER BY total_deliveries DESC;


SELECT
    delivery_partner,
    COUNT(*) AS total_deliveries,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delivered'
    ) AS delivered,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delayed'
    ) AS delayed,

    COUNT(*) FILTER (
        WHERE delivery_status = 'failed'
    ) AS failed,

    ROUND(AVG(delivery_cost), 2) AS average_cost,

    ROUND(AVG(delivery_rating), 2) AS average_rating

FROM delivery_analysis
GROUP BY delivery_partner
ORDER BY total_deliveries DESC;


SELECT
    vehicle_type,
    COUNT(*) AS total_deliveries,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delivered'
    ) AS delivered,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delayed'
    ) AS delayed,

    COUNT(*) FILTER (
        WHERE delivery_status = 'failed'
    ) AS failed,

    ROUND(AVG(distance_km), 2) AS average_distance_km,

    ROUND(AVG(delivery_cost), 2) AS average_delivery_cost

FROM delivery_analysis
GROUP BY vehicle_type
ORDER BY total_deliveries DESC;


SELECT
    weather_condition,
    COUNT(*) AS total_deliveries,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delivered'
    ) AS delivered,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delayed'
    ) AS delayed,

    COUNT(*) FILTER (
        WHERE delivery_status = 'failed'
    ) AS failed,

    ROUND(
        COUNT(*) FILTER (
            WHERE delivery_status IN ('delayed', 'failed')
        ) * 100.0 / COUNT(*),
        2
    ) AS delay_failure_percentage

FROM delivery_analysis
GROUP BY weather_condition
ORDER BY delay_failure_percentage DESC;


SELECT
    package_type,
    COUNT(*) AS total_deliveries,

    ROUND(AVG(package_weight_kg), 2) AS average_weight_kg,

    ROUND(AVG(distance_km), 2) AS average_distance_km,

    ROUND(AVG(delivery_cost), 2) AS average_delivery_cost,

    ROUND(AVG(delivery_rating), 2) AS average_rating,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delayed'
    ) AS delayed,

    COUNT(*) FILTER (
        WHERE delivery_status = 'failed'
    ) AS failed

FROM delivery_analysis
GROUP BY package_type
ORDER BY total_deliveries DESC;


SELECT
    delivery_mode,
    COUNT(*) AS total_deliveries,
    ROUND(AVG(delivery_cost), 2) AS average_cost,
    ROUND(MIN(delivery_cost), 2) AS minimum_cost,
    ROUND(MAX(delivery_cost), 2) AS maximum_cost,
    ROUND(AVG(distance_km), 2) AS average_distance_km,
    ROUND(AVG(package_weight_kg), 2) AS average_weight_kg
FROM delivery_analysis
GROUP BY delivery_mode
ORDER BY average_cost DESC;


SELECT
    CASE
        WHEN distance_km <= 50 THEN '0–50 km'
        WHEN distance_km <= 100 THEN '51–100 km'
        WHEN distance_km <= 200 THEN '101–200 km'
        ELSE 'Above 200 km'
    END AS distance_range,

    COUNT(*) AS total_deliveries,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delivered'
    ) AS delivered,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delayed'
    ) AS delayed,

    COUNT(*) FILTER (
        WHERE delivery_status = 'failed'
    ) AS failed,

    ROUND(AVG(delivery_cost), 2) AS average_cost

FROM delivery_analysis
GROUP BY distance_range
ORDER BY MIN(distance_km);


-- View 1: Delivery Status Summary
CREATE OR REPLACE VIEW vw_delivery_status AS
SELECT
    delivery_status,
    COUNT(*) AS total_deliveries,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM delivery_analysis
GROUP BY delivery_status;


SELECT *
FROM vw_delivery_status;


-- View 2: Delivery Partner Performance
CREATE OR REPLACE VIEW vw_partner_performance AS
SELECT
    delivery_partner,
    COUNT(*) AS total_deliveries,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delivered'
    ) AS delivered,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delayed'
    ) AS delayed,

    COUNT(*) FILTER (
        WHERE delivery_status = 'failed'
    ) AS failed,

    ROUND(AVG(delivery_cost), 2) AS average_cost,
    ROUND(AVG(delivery_rating), 2) AS average_rating

FROM delivery_analysis
GROUP BY delivery_partner;


SELECT *
FROM vw_partner_performance
ORDER BY total_deliveries DESC;


-- View 3: Regional Performance
CREATE OR REPLACE VIEW vw_regional_performance AS
SELECT
    region,
    COUNT(*) AS total_deliveries,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delivered'
    ) AS delivered,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delayed'
    ) AS delayed,

    COUNT(*) FILTER (
        WHERE delivery_status = 'failed'
    ) AS failed,

    ROUND(AVG(delivery_cost), 2) AS average_cost,
    ROUND(AVG(delivery_rating), 2) AS average_rating

FROM delivery_analysis
GROUP BY region;


SELECT *
FROM vw_regional_performance
ORDER BY total_deliveries DESC;


-- View 4: Dashboard KPI Summary
CREATE OR REPLACE VIEW vw_delivery_kpis AS
SELECT
    COUNT(*) AS total_deliveries,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delivered'
    ) AS delivered,

    COUNT(*) FILTER (
        WHERE delivery_status = 'delayed'
    ) AS delayed,

    COUNT(*) FILTER (
        WHERE delivery_status = 'failed'
    ) AS failed,

    ROUND(AVG(delivery_cost), 2) AS average_delivery_cost,

    ROUND(AVG(delivery_rating), 2) AS average_customer_rating

FROM delivery_analysis;


SELECT *
FROM vw_delivery_kpis;