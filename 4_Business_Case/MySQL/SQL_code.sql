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


# Locating IT Departments from US with actual spending over planned budget

SELECT 
    actuals.date,
    actuals.it_department,
    SUM(actuals.actual) AS actual,
    SUM(budget.budget) AS budget,
    SUM(budget.budget) - SUM(actuals.actual) AS difference
FROM
    departments
        JOIN
    actuals ON departments.it_department = actuals.it_department
        JOIN
    budget ON departments.it_department = budget.it_department
WHERE
    actuals.country = 'USA'
GROUP BY departments.it_department , actuals.date
HAVING difference < 0;


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