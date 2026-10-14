WITH date_spine AS (

    SELECT explode(
        sequence(
            to_date('2024-01-01'),
            to_date('2026-12-31'),
            interval 1 day
        )
    ) AS date_day

)

SELECT
    date_day AS date_key,
    YEAR(date_day) AS year,
    MONTH(date_day) AS month,
    DAY(date_day) AS day,
    QUARTER(date_day) AS quarter,
    DATE_FORMAT(date_day, 'EEEE') AS day_name,
    DATE_FORMAT(date_day, 'MMMM') AS month_name,
    WEEKOFYEAR(date_day) AS week_of_year

FROM date_spine