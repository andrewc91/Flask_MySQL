SELECT countries.name, languages.language, languages.percentage
FROM languages
JOIN countries ON countries.id = languages.country_id
WHERE languages.language = 'Slovene' 
ORDER BY languages.percentage DESC 

SELECT countries.name, COUNT()
FROM cities
JOIN countries ON countries.id = cities.country_id
GROUP BY countries.names ORDER BY COUNT() DESC

SELECT cities.name, cities.population
FROM cities
JOIN countries on countries.id = cities.country_id
WHERE countries.name = 'Mexico' and cities.population > 500000
ORDER BY cities.population DESC

SELECT countries.name, languages.language, languages.percentage
FROM languages
JOIN countries ON countries.id = languages.country_id
WHERE languages.percentage > 89
ORDER BY languages.percentage DESC

SELECT name, surface_area, population
FROM countries
WHERE surface_area < 501 AND population > 100000

SELECT name, government_form, capital, life_expectancy
FROM countries
WHERE government_form = 'Constitutional Monarchy' AND capital > 200 AND life_expectancy > 75

SELECT countries.name, cities.name, cities.district, cities.population
FROM cities
JOIN countries ON countries.id = cities.country_id
WHERE cities.population > 500000 and cities.district = 'Buenos Aires'

SELECT region, COUNT(name)
FROM countries
GROUP BY (region) 
ORDER BY COUNT(name) DESC
