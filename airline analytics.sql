CREATE DATABASE airline_analytics;
USE airline_analytics;
CREATE TABLE airlines (
    airline_id INT PRIMARY KEY,
    airline_name VARCHAR(100),
    rating DECIMAL(2,1)
);
CREATE TABLE airports (
    airport_id INT PRIMARY KEY,
    airport_name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50)
);
CREATE TABLE flights (
    flight_id INT PRIMARY KEY,
    airline_id INT,
    departure_airport INT,
    arrival_airport INT,
    departure_time TIME,
    arrival_time TIME,
    duration INT,
    FOREIGN KEY (airline_id) REFERENCES airlines(airline_id),
    FOREIGN KEY (departure_airport) REFERENCES airports(airport_id),
    FOREIGN KEY (arrival_airport) REFERENCES airports(airport_id)
);
Drop table passengers;
CREATE TABLE passengers (
    passenger_id INT PRIMARY KEY,
    name VARCHAR(100),
    gender VARCHAR(10),
    age INT,
    nationality VARCHAR(50)
);
Drop table bookings;
CREATE TABLE bookings (
    booking_id INT PRIMARY KEY auto_increment,
    passenger_id INT,
    flight_id INT,
    booking_date DATE,
    ticket_price DECIMAL(10,2),
    FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
);
INSERT INTO airlines VALUES
(1,'Emirates',4.8),
(2,'Indigo',4.2),
(3,'Qatar Airways',4.7),
(4,'Air India',4.0);
select*from airlines;
Delete  from airlines Where airline_id is Null;
INSERT INTO airports VALUES
(1,'Indira Gandhi International Airport','Delhi','India'),
(2,'Dubai International Airport','Dubai','UAE'),
(3,'Chhatrapati Shivaji Airport','Mumbai','India'),
(4,'Heathrow Airport','London','UK'),
(5,'Changi Airport','Singapore','Singapore'),
(6,'Hamad International Airport','Doha','Qatar'),
(7,'John F Kennedy Airport','New York','USA'),
(8,'Los Angeles International Airport','Los Angeles','USA');
SELECT * FROM airports;
INSERT INTO flights VALUES
(101,1,1,2,'08:00:00','11:30:00',210),
(102,2,3,2,'09:30:00','12:30:00',180),
(103,3,1,4,'10:00:00','18:00:00',480),
(104,4,3,1,'07:00:00','09:00:00',120),
(105,1,2,7,'13:00:00','22:00:00',540),
(106,3,6,4,'06:00:00','14:00:00',480),
(107,2,1,3,'15:00:00','17:00:00',120),
(108,4,3,5,'11:00:00','19:00:00',480);
Select * from flights;
INSERT INTO passengers VALUES
(1,'Rahul Sharma','Male',32,'India'),
(2,'Ananya Patel','Female',27,'India'),
(3,'David Smith','Male',40,'UK'),
(4,'Sara Khan','Female',29,'UAE'),
(5,'Michael Johnson','Male',45,'USA'),
(6,'Priya Nair','Female',31,'India'),
(7,'Ahmed Ali','Male',36,'Qatar'),
(8,'Emily Brown','Female',28,'UK');
INSERT INTO bookings (passenger_id, flight_id, booking_date, ticket_price) VALUES
(1,101,'2024-03-01',25000),
(2,102,'2024-03-02',18000),
(3,103,'2024-03-03',52000),
(4,101,'2024-03-04',26000),
(5,105,'2024-03-05',60000),
(6,104,'2024-03-06',15000),
(7,106,'2024-03-07',48000),
(8,108,'2024-03-08',42000);
SELECT                                         
a1.city AS Departure,
a2.city AS Arrival,
COUNT(b.booking_id) AS Total_Passengers
FROM bookings b
JOIN flights f ON b.flight_id = f.flight_id
JOIN airports a1 ON f.departure_airport = a1.airport_id
JOIN airports a2 ON f.arrival_airport = a2.airport_id
GROUP BY a1.city, a2.city
ORDER BY Total_Passengers DESC;
SELECT COUNT(*) AS Total_Bookings FROM bookings;
SELECT SUM(ticket_price) AS Total_Revenue FROM bookings;
SELECT AVG(ticket_price) AS Avg_Price FROM bookings;
SELECT airline_id, COUNT(*) AS Flights_Count
FROM flights
GROUP BY airline_id
ORDER BY Flights_Count DESC;
ALTER TABLE passengers MODIFY passenger_id INT AUTO_INCREMENT;
ALTER TABLE bookings DROP FOREIGN KEY bookings_ibfk_1;
ALTER TABLE bookings
ADD CONSTRAINT fk_passenger
FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id);


