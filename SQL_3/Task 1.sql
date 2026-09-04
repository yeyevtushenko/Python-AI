CREATE DATABASE Academy;

CREATE TABLE Departments (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Financing MONEY NOT NULL DEFAULT 0,
    Name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Faculties (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Dean VARCHAR(255) NOT NULL,
    Name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Groups (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(10) NOT NULL UNIQUE,
    Rating INT NOT NULL CHECK (Rating >= 0 AND Rating <= 5),
    Year INT NOT NULL CHECK (Year >= 1 AND Year <= 5)
);

CREATE TABLE Teachers (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    EmploymentDate DATE NOT NULL CHECK (EmploymentDate >= '1990-01-01'),
    IsAssistant BIT NOT NULL DEFAULT 0,
    IsProfessor BIT NOT NULL DEFAULT 0,
    Name NVARCHAR(MAX) NOT NULL,
    Position VARCHAR(MAX) NOT NULL,
    Premium MONEY NOT NULL DEFAULT 0,
    Salary MONEY NOT NULL CHECK (Salary > 0),
    Surname VARCHAR(MAX) NOT NULL
);

SELECT * FROM Departments ORDER BY Id DESC;
SELECT Name AS "Group Name", Rating AS "Group Rating" FROM Groups;
SELECT Surname, (Premium / Salary) * 100 AS "Premium as % of Salary", ((Premium + Salary) / Salary) * 100 AS "Total Pay as % of Salary" FROM Teachers;
SELECT CONCAT('The dean of faculty ', Name, ' is ', Dean, '.') AS "Faculty Information" FROM Faculties;
SELECT Surname FROM Teachers WHERE Salary > 1050 AND IsProfessor = 1;
SELECT Name FROM Departments WHERE Financing < 11000 OR Financing > 25000;
SELECT Name FROM Faculties WHERE Name <> 'Computer Science';
SELECT Surname, Position FROM Teachers WHERE IsProfessor = 0;
SELECT Surname, Position, Salary, Premium FROM Teachers WHERE IsAssistant = 1 AND Premium BETWEEN 160 AND 550;
SELECT Surname, Salary FROM Teachers WHERE IsAssistant = 1;
SELECT Surname, Position FROM Teachers WHERE EmploymentDate < '2000-01-01';
SELECT Name AS "Name of Department" FROM Departments WHERE Name < 'Software Development' ORDER BY Name;
SELECT Surname FROM Teachers WHERE IsAssistant = 1 AND (Salary + Premium) <= 1200;
SELECT Name FROM Groups WHERE Year = 5 AND Rating BETWEEN 2 AND 4;
SELECT Surname FROM Teachers WHERE IsAssistant = 1 AND (Salary < 550 OR Premium < 200);