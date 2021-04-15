### Creating tables


DROP TABLE IF EXISTS cost_elements;
CREATE TABLE cost_elements (
    cost_element VARCHAR(25) PRIMARY KEY,
    cost_element_group VARCHAR(25),
    business_area VARCHAR(25)
    );
    
DROP TABLE IF EXISTS departments;
CREATE TABLE departments (
    it_department VARCHAR(25) PRIMARY KEY,
    it_area VARCHAR(25),
    dept_manager VARCHAR(25)
    );

DROP TABLE IF EXISTS regions;
CREATE TABLE regions (
    country VARCHAR(25) PRIMARY KEY,
    region VARCHAR(25)
    );
    
DROP TABLE IF EXISTS actuals;
CREATE TABLE actuals (
    date VARCHAR(25),
    it_department VARCHAR(25),
    cost_element VARCHAR(25),
    country VARCHAR(25),
    actual VARCHAR(25),
    FOREIGN KEY (it_department) REFERENCES departments(it_department),
    FOREIGN KEY (cost_element) REFERENCES cost_elements(cost_element),
    FOREIGN KEY (country) REFERENCES regions(country)
    );
    
DROP TABLE IF EXISTS budget;
CREATE TABLE budget (
    date VARCHAR(25),
    it_department VARCHAR(25),
    cost_element VARCHAR(25),
    country VARCHAR(25),
    budget VARCHAR(25),
    FOREIGN KEY (it_department) REFERENCES departments(it_department),
    FOREIGN KEY (cost_element) REFERENCES cost_elements(cost_element),
    FOREIGN KEY (country) REFERENCES regions(country)
    );

DROP TABLE IF EXISTS forecast;
CREATE TABLE forecast (
    date VARCHAR(25),
    it_department VARCHAR(25),
    cost_element VARCHAR(25),
    country VARCHAR(25),
    forecast VARCHAR(25),
    FOREIGN KEY (it_department) REFERENCES departments(it_department),
    FOREIGN KEY (cost_element) REFERENCES cost_elements(cost_element),
    FOREIGN KEY (country) REFERENCES regions(country)
    );


### Loading the data into tables


SET GLOBAL local_infile=1;

LOAD DATA LOCAL INFILE 'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\Actuals.csv' INTO TABLE actuals
FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\Budget.csv' INTO TABLE budget;
LOAD DATA LOCAL INFILE 'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\Cost_Element.csv' INTO TABLE cost_element;
LOAD DATA LOCAL INFILE 'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\IT_Department.csv' INTO TABLE departments;
LOAD DATA LOCAL INFILE 'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\Forecast.csv' INTO TABLE forecast;
LOAD DATA LOCAL INFILE 'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\Country.csv' INTO TABLE regions;
	


### Cleaning the data


SET SQL_SAFE_UPDATES = 0;

UPDATE actuals
	SET actual = REPLACE(actual,',','') 
	WHERE actual LIKE '%,%'; 
ALTER TABLE actuals
	MODIFY COLUMN actual INT;

UPDATE actuals
	SET date =  STR_TO_DATE(date, '%d/%m/%Y');
ALTER TABLE actuals
	MODIFY COLUMN date DATE;

UPDATE budget
	SET budget = REPLACE(budget,',','') 
	WHERE budget LIKE '%,%';
ALTER TABLE budget
	MODIFY COLUMN budget INT;

UPDATE budget
	SET date =  STR_TO_DATE(date, '%d/%m/%Y');
ALTER TABLE budget
	MODIFY COLUMN date DATE;

UPDATE forecast
	SET forecast = REPLACE(forecast,',','') 
	WHERE forecast LIKE '%,%';
ALTER TABLE forecast
	MODIFY COLUMN forecast INT;

UPDATE forecast
	SET date =  STR_TO_DATE(date, '%d/%m/%Y');
ALTER TABLE forecast
	MODIFY COLUMN date DATE;


### Quering the data

# Finding IT departments with biggest percentage difference between actual spending and budget for first 7 months of the year

SELECT 
    a.country,
    a.it_department,
    SUM(a.actual) AS actual,
    SUM(b.budget) AS budget,
    ROUND(SUM(a.actual) / SUM(b.budget) * 100) AS percentage_ratio
FROM
    actuals a
        LEFT JOIN
    budget b ON (a.date = b.date
        AND a.it_department = b.it_department
        AND a.country = b.country
        AND a.cost_element = b.cost_element)
GROUP BY a.it_department , a.country
ORDER BY percentage_ratio DESC , a.country;
    


# Presenting elements of the region with biggest expected spending comparing to the budget from month of July onwards

SELECT 
    b.cost_element,
    r.region,
    SUM(b.budget) AS budget,
    SUM(f.forecast) AS forecast,
    ROUND(SUM(f.forecast) / SUM(b.budget) * 100) AS percentage_ratio
FROM
    budget AS b
        JOIN
    forecast AS f ON (b.date = f.date
        AND b.it_department = f.it_department
        AND b.country = f.country
        AND b.cost_element = f.cost_element)
        JOIN
    regions AS r ON b.country = r.country
WHERE b.date BETWEEN '2020-08-01' AND '2020-12-30'
GROUP BY b.cost_element , r.region
HAVING percentage_ratio > 130
ORDER BY percentage_ratio DESC ;

      


# Presenting budget for Hardware and Software Maintenance for individual countries

SELECT 
    budget.country, 
    regions.region, 
    SUM(budget.budget) AS budget
FROM
    regions
        JOIN
    budget ON regions.country = budget.country
WHERE
    budget.cost_element LIKE '%Maintenance'
GROUP BY budget.country;
