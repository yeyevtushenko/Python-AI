SELECT COUNT(*) AS NumberOfVegetables
FROM vegetables_and_fruits
WHERE Type = 'овоч';

SELECT COUNT(*) AS NumberOfFruits
FROM vegetables_and_fruits
WHERE Type = 'фрукт';

SELECT COUNT(*) AS NumberOfItems
FROM vegetables_and_fruits
WHERE Color = 'червоний';

SELECT Color, COUNT(*) AS NumberOfItems
FROM vegetables_and_fruits
GROUP BY Color;

SELECT Color, COUNT(*) AS NumberOfItems
FROM vegetables_and_fruits
GROUP BY Color
ORDER BY NumberOfItems ASC
LIMIT 1;

SELECT Color, COUNT(*) AS NumberOfItems
FROM vegetables_and_fruits
GROUP BY Color
ORDER BY NumberOfItems DESC
LIMIT 1;

SELECT MIN(Calories) AS MinCalories
FROM vegetables_and_fruits;

SELECT MAX(Calories) AS MaxCalories
FROM vegetables_and_fruits;

SELECT AVG(Calories) AS AverageCalories
FROM vegetables_and_fruits;

SELECT Name, Calories
FROM vegetables_and_fruits
WHERE Type = 'фрукт'
ORDER BY Calories ASC
LIMIT 1;

SELECT Name, Calories
FROM vegetables_and_fruits
WHERE Type = 'фрукт'
ORDER BY Calories DESC
LIMIT 1;