# E-Commerce Sales & Customer Analytics

An end-to-end Data Analytics project analyzing Brazilian e-commerce data to uncover sales trends, customer behavior, product performance, geographic patterns, and order performance.

The project demonstrates a complete analytics workflow using **Python, SQL, Power BI, Pandas, and Data Visualization**.

## Project Objective

The objective of this project is to transform raw e-commerce data into meaningful business insights and answer questions such as:

- How is revenue changing over time?
- Which product categories generate the most revenue?
- Which states contribute the most orders?
- What is the overall order fulfillment performance?
- How many unique customers purchase from the platform?
- What is the average value generated per order?

## Tools & Technologies

- **Python** — Data cleaning, EDA and feature engineering
- **Pandas & NumPy** — Data manipulation and analysis
- **Matplotlib** — Data visualization
- **SQL / MySQL** — Business queries and relational analysis
- **Power BI** — Interactive dashboard and KPI reporting
- **DAX** — Business measures and KPIs
- **Git & GitHub** — Project documentation and version control

## Dataset

The project uses the Brazilian E-Commerce Public Dataset by Olist.

The dataset contains approximately **100K orders** and multiple relational tables covering:

- Customers
- Orders
- Order Items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Product Category Translation

## Data Analysis Workflow

### 1. Data Preparation

The raw datasets were inspected for:

- Missing values
- Duplicate records
- Incorrect data types
- Date/time consistency
- Data quality issues

Missing values were handled based on their business meaning rather than blindly deleting records.

### 2. Exploratory Data Analysis

Python was used to analyze:

- Monthly revenue and order trends
- Top product categories
- Delivery performance
- Customer and order patterns
- Data distributions and quality

Feature engineering was performed to create:

- Order year and month
- Delivery duration
- Delivery delay
- Delivery performance status

### 3. SQL Analysis

SQL was used to perform relational business analysis across multiple tables, including:

- Revenue analysis
- Customer analysis
- Order trends
- Product/category performance
- Geographic analysis
- Payment and order behavior

### 4. Power BI Dashboard

An interactive Power BI dashboard was created to summarize the most important business KPIs and trends.

Key KPIs include:

- **Total Revenue**
- **Total Orders**
- **Total Customers**
- **Average Order Value**

The dashboard also includes:

- Revenue trend over time
- Top product categories by revenue
- Orders by customer state
- Order status distribution
- Year-based filtering

## Dashboard

![Power BI Dashboard](images/powerbi_dashboard.png)

## Key Business Insights

- The business experienced substantial growth in order volume and revenue during the main operating period.
- Revenue is concentrated among several high-performing product categories.
- São Paulo (SP) contributes the largest share of customer orders, making it a key geographic market.
- The overwhelming majority of orders are successfully delivered, indicating strong overall fulfillment performance.
- Geographic and category-level differences provide opportunities for targeted marketing and regional growth strategies.
- Monitoring delivery performance alongside customer reviews can help identify opportunities to improve customer satisfaction.

## Repository Structure

    E-Commerce-Sales-Customer-Analytics/
    |
    ├── data/          # Dataset information / data files
    ├── notebooks/     # Python EDA and analysis
    ├── sql/           # SQL analysis queries
    ├── dashboard/     # Power BI dashboard files/information
    ├── images/        # Dashboard screenshots
    └── README.md      # Project documentation

## Skills Demonstrated

**Data Cleaning | Exploratory Data Analysis | SQL | Python | Pandas | Data Visualization | Power BI | DAX | Data Modeling | Business Analysis**

## Project Outcome

This project demonstrates an end-to-end data analytics workflow—from raw relational data and data cleaning to SQL analysis, exploratory analysis, KPI development, dashboard creation, and business insight generation.
