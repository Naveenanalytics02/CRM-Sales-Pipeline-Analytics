-- Overall sales pipeline summary

SELECT
    COUNT(*) AS total_opportunities,
    COUNT(*) FILTER (WHERE deal_stage = 'Won') AS won_deals,
    COUNT(*) FILTER (WHERE deal_stage = 'Lost') AS lost_deals,
    COUNT(*) FILTER (WHERE deal_stage = 'Engaging') AS engaging_deals,
    COUNT(*) FILTER (WHERE deal_stage = 'Prospecting') AS prospecting_deals,
    SUM(close_value) FILTER (WHERE deal_stage = 'Won') AS total_won_revenue,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE deal_stage = 'Won')
        / COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost')),
        2
    ) AS win_rate
FROM sales_pipeline;

-- Opportunities and revenue by deal stage

SELECT
    deal_stage,
    COUNT(*) AS total_opportunities,
    SUM(close_value) AS total_revenue,
    ROUND(AVG(close_value), 2) AS average_deal_value
FROM sales_pipeline
GROUP BY deal_stage
ORDER BY total_opportunities DESC;

-- Product performance

SELECT
    product,
    COUNT(*) AS total_opportunities,
    COUNT(*) FILTER (WHERE deal_stage = 'Won') AS won_deals,
    SUM(close_value) FILTER (WHERE deal_stage = 'Won') AS won_revenue,
    ROUND(
        AVG(close_value) FILTER (WHERE deal_stage = 'Won'),
        2
    ) AS average_won_deal
FROM sales_pipeline
GROUP BY product
ORDER BY won_revenue DESC;

-- Product win rate

SELECT
    product,
    COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost')) AS completed_deals,
    COUNT(*) FILTER (WHERE deal_stage = 'Won') AS won_deals,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE deal_stage = 'Won')
        / NULLIF(COUNT(*) FILTER (WHERE deal_stage IN ('Won', 'Lost')), 0),
        2
    ) AS win_rate
FROM sales_pipeline
GROUP BY product
ORDER BY win_rate DESC;