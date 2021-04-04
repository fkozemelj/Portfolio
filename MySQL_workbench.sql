CREATE TABLE station (
    id INT PRIMARY KEY,
    station VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT,
    dock_count INT,
    city VARCHAR(30),
    installation_date VARCHAR(15));
    

SELECT * FROM station