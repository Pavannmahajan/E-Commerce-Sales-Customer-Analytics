-- ============================================================
-- E-COMMERCE SALES & CUSTOMER ANALYTICS
-- SQL Business Analysis
-- Dataset: Brazilian E-Commerce Public Dataset by Olist
-- ============================================================

USE ecommerce_analytics;

-- ============================================================
-- 1. TOTAL ORDERS
-- ============================================================

SELECT 
    COUNT(DISTINCT order_id) AS total_orders
FROM olist_orders_dataset;


-- ============================================================
-- 2. TOTAL UNIQUE CUSTOMERS
-- ============================================================

SELECT 
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM olist_customers_dataset;


-- ============================================================
-- 3. ORDERS BY STATUS
-- ============================================================

SELECT 
    order_status,
    COUNT(DISTINCT order_id) AS total_orders
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY total_orders DESC;


-- ============================================================
-- 4. ORDERS BY YEAR
-- ============================================================

SELECT
    YEAR(order_purchase_timestamp) AS order_year,
    COUNT(DISTINCT order_id) AS total_orders
FROM olist_orders_dataset
GROUP BY YEAR(order_purchase_timestamp)
ORDER BY order_year;


-- ============================================================
-- 5. ORDERS BY MONTH
-- ============================================================

SELECT
    DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS order_month,
    COUNT(DISTINCT order_id) AS total_orders
FROM olist_orders_dataset
GROUP BY DATE_FORMAT(order_purchase_timestamp, '%Y-%m')
ORDER BY order_month;


-- ============================================================
-- 6. TOTAL REVENUE FROM ORDER ITEMS
-- ============================================================

SELECT
    ROUND(SUM(price), 2) AS total_revenue
FROM olist_order_items_dataset;


-- ============================================================
-- 7. AVERAGE ORDER VALUE
-- Revenue per unique order
-- ============================================================

SELECT
    ROUND(
        SUM(price) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM olist_order_items_dataset;


-- ============================================================
-- 8. REVENUE BY YEAR
-- ============================================================

SELECT
    YEAR(o.order_purchase_timestamp) AS order_year,
    ROUND(SUM(oi.price), 2) AS total_revenue
FROM olist_orders_dataset o
JOIN olist_order_items_dataset oi
    ON o.order_id = oi.order_id
GROUP BY YEAR(o.order_purchase_timestamp)
ORDER BY order_year;


-- ============================================================
-- 9. MONTHLY REVENUE TREND
-- ============================================================

SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS order_month,
    ROUND(SUM(oi.price), 2) AS total_revenue
FROM olist_orders_dataset o
JOIN olist_order_items_dataset oi
    ON o.order_id = oi.order_id
GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
ORDER BY order_month;


-- ============================================================
-- 10. TOP 10 CUSTOMER CITIES
-- ============================================================

SELECT
    customer_city,
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM olist_customers_dataset
GROUP BY customer_city
ORDER BY total_customers DESC
LIMIT 10;


-- ============================================================
-- 11. ORDERS BY CUSTOMER STATE
-- ============================================================

SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM olist_orders_dataset o
JOIN olist_customers_dataset c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY total_orders DESC;


-- ============================================================
-- 12. TOP PRODUCT CATEGORIES BY REVENUE
-- ============================================================

SELECT
    p.product_category_name,
    ROUND(SUM(oi.price), 2) AS total_revenue
FROM olist_order_items_dataset oi
JOIN olist_products_dataset p
    ON oi.product_id = p.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================
-- 13. TOP PRODUCT CATEGORIES BY ITEMS SOLD
-- ============================================================

SELECT
    p.product_category_name,
    COUNT(*) AS total_items_sold
FROM olist_order_items_dataset oi
JOIN olist_products_dataset p
    ON oi.product_id = p.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY total_items_sold DESC
LIMIT 10;


-- ============================================================
-- 14. PAYMENT METHOD ANALYSIS
-- ============================================================

SELECT
    payment_type,
    COUNT(*) AS total_transactions,
    ROUND(SUM(payment_value), 2) AS total_payment_value
FROM olist_order_payments_dataset
GROUP BY payment_type
ORDER BY total_payment_value DESC;


-- ============================================================
-- 15. CUSTOMER REVIEW SCORE DISTRIBUTION
-- ============================================================

SELECT
    review_score,
    COUNT(*) AS total_reviews
FROM olist_order_reviews_dataset
GROUP BY review_score
ORDER BY review_score;


-- ============================================================
-- 16. AVERAGE REVIEW SCORE
-- ============================================================

SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM olist_order_reviews_dataset;


-- ============================================================
-- 17. DELIVERY PERFORMANCE
-- Average actual delivery duration in days
-- ============================================================

SELECT
    ROUND(
        AVG(
            DATEDIFF(
                order_delivered_customer_date,
                order_purchase_timestamp
            )
        ),
        2
    ) AS avg_delivery_days
FROM olist_orders_dataset
WHERE order_delivered_customer_date IS NOT NULL;


-- ============================================================
-- 18. ON-TIME VS LATE DELIVERIES
-- ============================================================

SELECT
    CASE
        WHEN order_delivered_customer_date <= order_estimated_delivery_date
            THEN 'On Time'
        ELSE 'Late'
    END AS delivery_status,
    COUNT(*) AS total_orders
FROM olist_orders_dataset
WHERE order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL
GROUP BY delivery_status
ORDER BY total_orders DESC;


-- ============================================================
-- END OF ANALYSIS
-- ============================================================