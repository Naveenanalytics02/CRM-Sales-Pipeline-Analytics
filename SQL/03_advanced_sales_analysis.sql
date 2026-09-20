-- Rank sales agents by win rate

WITH agent_performance AS (
    SELECT
        sales_agent,
        COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost')) AS completed_deals,
        COUNT(*) FILTER (WHERE deal_stage = 'Won') AS won_deals,
        ROUND(
            100.0 * COUNT(*) FILTER (WHERE deal_stage = 'Won')
            / NULLIF(COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost')), 0),
            2
        ) AS win_rate
    FROM sales_pipeline
    GROUP BY sales_agent
)

SELECT
    sales_agent,
    completed_deals,
    won_deals,
    win_rate,
    RANK() OVER (ORDER BY win_rate DESC) AS performance_rank
FROM agent_performance
ORDER BY performance_rank;

-- Manager performance analysis

WITH manager_performance AS (
    SELECT
        st.manager,
        COUNT(*) FILTER (
            WHERE sp.deal_stage IN ('Won', 'Lost')
        ) AS completed_deals,

        COUNT(*) FILTER (
            WHERE sp.deal_stage = 'Won'
        ) AS won_deals,

        SUM(sp.close_value) FILTER (
            WHERE sp.deal_stage = 'Won'
        ) AS won_revenue,

        ROUND(
            100.0 * COUNT(*) FILTER (WHERE sp.deal_stage = 'Won')
            / NULLIF(
                COUNT(*) FILTER (
                    WHERE sp.deal_stage IN ('Won', 'Lost')
                ),
                0
            ),
            2
        ) AS win_rate

    FROM sales_pipeline sp
    JOIN sales_teams st
        ON sp.sales_agent = st.sales_agent

    GROUP BY st.manager
)

SELECT
    manager,
    completed_deals,
    won_deals,
    won_revenue,
    win_rate,

    RANK() OVER (
        ORDER BY win_rate DESC
    ) AS performance_rank

FROM manager_performance
ORDER BY performance_rank;

-- Monthly sales performance

WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', close_date) AS sales_month,
        COUNT(*) AS won_deals,
        SUM(close_value) AS won_revenue
    FROM sales_pipeline
    WHERE deal_stage = 'Won'
    GROUP BY DATE_TRUNC('month', close_date)
)

SELECT
    sales_month,
    won_deals,
    won_revenue,
    SUM(won_revenue) OVER (
        ORDER BY sales_month
    ) AS cumulative_revenue
FROM monthly_sales
ORDER BY sales_month;

-- Regional sales performance

SELECT
    st.regional_office,
    COUNT(*) FILTER (
        WHERE sp.deal_stage IN ('Won', 'Lost')
    ) AS completed_deals,
    COUNT(*) FILTER (
        WHERE sp.deal_stage = 'Won'
    ) AS won_deals,
    SUM(sp.close_value) FILTER (
        WHERE sp.deal_stage = 'Won'
    ) AS won_revenue,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE sp.deal_stage = 'Won'
        )
        / NULLIF(
            COUNT(*) FILTER (
                WHERE sp.deal_stage IN ('Won', 'Lost')
            ), 0
        ),
        2
    ) AS win_rate
FROM sales_pipeline sp
JOIN sales_teams st
    ON sp.sales_agent = st.sales_agent
GROUP BY st.regional_office
ORDER BY win_rate DESC;

-- Account performance analysis

SELECT
    sp.account,
    COUNT(*) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')) AS completed_deals,
    COUNT(*) FILTER (WHERE sp.deal_stage = 'Won') AS won_deals,
    SUM(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won') AS won_revenue,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE sp.deal_stage = 'Won')
        / NULLIF(COUNT(*) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')), 0),
        2
    ) AS win_rate
FROM sales_pipeline sp
WHERE sp.account <> 'Unknown'
GROUP BY sp.account
ORDER BY won_revenue DESC;

-- Sector performance analysis

SELECT
    a.sector,
    COUNT(*) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')) AS completed_deals,
    COUNT(*) FILTER (WHERE sp.deal_stage = 'Won') AS won_deals,
    SUM(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won') AS won_revenue,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE sp.deal_stage = 'Won')
        / NULLIF(
            COUNT(*) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')),
            0
        ),
        2
    ) AS win_rate
FROM sales_pipeline sp
JOIN accounts a
    ON sp.account = a.account
GROUP BY a.sector
ORDER BY win_rate DESC;

-- Product series performance

SELECT
    p.series,
    COUNT(*) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')) AS completed_deals,
    COUNT(*) FILTER (WHERE sp.deal_stage = 'Won') AS won_deals,
    SUM(sp.close_value) FILTER (WHERE sp.deal_stage = 'Won') AS won_revenue,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE sp.deal_stage = 'Won')
        / NULLIF(COUNT(*) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')), 0),
        2
    ) AS win_rate
FROM sales_pipeline sp
JOIN products p
    ON sp.product = p.product
GROUP BY p.series
ORDER BY win_rate DESC;

-- Deal cycle time analysis

SELECT
    product,
    COUNT(*) AS won_deals,
    ROUND(AVG(close_date - engage_date), 2) AS average_days_to_close,
    MIN(close_date - engage_date) AS fastest_days,
    MAX(close_date - engage_date) AS longest_days
FROM sales_pipeline
WHERE deal_stage = 'Won'
  AND engage_date IS NOT NULL
  AND close_date IS NOT NULL
GROUP BY product
ORDER BY average_days_to_close;

-- High-value account analysis

SELECT
    sp.account,
    COUNT(*) FILTER (
        WHERE sp.deal_stage IN ('Won', 'Lost')
    ) AS completed_deals,
    COUNT(*) FILTER (
        WHERE sp.deal_stage = 'Won'
    ) AS won_deals,
    SUM(sp.close_value) FILTER (
        WHERE sp.deal_stage = 'Won'
    ) AS won_revenue,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE sp.deal_stage = 'Won')
        / NULLIF(
            COUNT(*) FILTER (WHERE sp.deal_stage IN ('Won', 'Lost')),
            0
        ),
        2
    ) AS win_rate
FROM sales_pipeline sp
WHERE sp.account <> 'Unknown'
GROUP BY sp.account
ORDER BY won_revenue DESC;