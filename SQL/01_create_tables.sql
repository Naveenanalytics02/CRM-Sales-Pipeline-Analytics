CREATE TABLE accounts (
    account VARCHAR(100) PRIMARY KEY,
    sector VARCHAR(50),
    year_established INT,
    revenue NUMERIC(12,2),
    employees INT,
    office_location VARCHAR(100),
    subsidiary_of VARCHAR(100)
);

CREATE TABLE products (
    product VARCHAR(100) PRIMARY KEY,
    series VARCHAR(50),
    sales_price NUMERIC(12,2)
);

CREATE TABLE sales_teams (
    sales_agent VARCHAR(100) PRIMARY KEY,
    manager VARCHAR(100),
    regional_office VARCHAR(100)
);
CREATE TABLE sales_pipeline (
    opportunity_id VARCHAR(50) PRIMARY KEY,
    sales_agent VARCHAR(100),
    product VARCHAR(100),
    account VARCHAR(100),
    deal_stage VARCHAR(50),
    engage_date DATE,
    close_date DATE,
    close_value NUMERIC(12,2)
);