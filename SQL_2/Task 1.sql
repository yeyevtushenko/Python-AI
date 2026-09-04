SELECT *
FROM vegetables_and_fruits
WHERE Type = 'овоч' AND Calories < 50;

SELECT *
FROM vegetables_and_fruits
WHERE Type = 'фрукт' AND Calories BETWEEN 50 AND 100;

SELECT *
FROM vegetables_and_fruits
WHERE Type = 'овоч' AND Name LIKE '%капуста%';

SELECT *
FROM vegetables_and_fruits
WHERE Description LIKE '%гемоглобін%';

SELECT *
FROM vegetables_and_fruits
WHERE Color IN ('жовтий', 'червоний');