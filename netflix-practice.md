State the criteria in English
Provide the SQL query that yields those results
Include a screenshot of this SQL query being issued in psql alongside the first few results


## 1. Movies filtered by title and/or year: A query that retrieves the ID, year, and title of movies that fit criteria of your choosing (e.g., movies with certain titles or title patterns, movies released on one or more given years, etc.), sorted ascending by title

Criteria: Movies that contain "the sequel" in the title.

SELECT * FROM movie WHERE title ILIKE '%the Sequel%' ORDER BY title;

![screenshot](/screenshots/netflix-query1.png)

## 2. Number of movies released per year: A query that takes movie criteria of your choosing and returns a table consisting of year and count where count is the number of movies that meet these criteria which were released on that year, sorted ascending by year

Criteria: List the count of movies per year from 1950-1999 that contained the " II" somewhere in the title (ie a search that looks for movies that might be a "part II" or "part III" type sequel with roman numberals in their titles, but technically also be Richard III)

SELECT year, COUNT(*) FROM movie WHERE title ILIKE '% II%' AND (year < 2000 AND year > 1949) GROUP BY year ORDER BY year;

![screenshot](/screenshots/netflix-query2.png)

## 3. Years with the most movies released: A query that takes movie criteria of your choosing and returns the same table as above except it only returns the year and count of the top five (5) years with the most movies released, sorted descending by count then ascending by year in case of a tie

Criteria: Same as above but limited to the top 5 years with the most " II" movies released, sorted descending by count then ascending by year in case of a tie.

SELECT year, COUNT(*) FROM movie WHERE title ILIKE '% II%' AND (year < 2000 AND year > 1949) GROUP BY year ORDER BY COUNT(*) DESC, year FETCH FIRST 5 ROWS ONLY;

![screenshot](/screenshots/netflix-query3.png)

## 4. Movies rated a certain way by a specific user: A query that lists the title and year of movies seen by a particular user with a rating matching conditions of your choosing (e.g., 4 and above, 2 and below, etc.) sorted ascending by title

Criteria: List the title and year of movies reviewed by user #1634777 that he/she rated 4 or higher.

SELECT title, year FROM movie INNER JOIN rating ON movie.id = rating.movie_id WHERE viewer_id = 1634777 AND rating > 3 ORDER BY title;

![screenshot](/screenshots/netflix-query4.png)

## 5.Average rating of movies: A query that takes movie criteria of your choosing and returns a table consisting of title, year, and avg where avg is the average rating received by each movie, sorted descending by avg (thus listing the top-rated movie first) then ascending by title in case of a tie

Criteria: List the title, year, and average rating of movies from 1980-2005(or technically until the end of the data) of movies with "robot" somewhere in the title, sorted descending by avg, then ascending by title in case of a tie.

SELECT year, title, AVG(rating) FROM movie, rating WHERE movie.id = rating.movie_id AND title ILIKE '%robot%' AND (year > 1979) GROUP BY title, year ORDER BY AVG(rating) DESC, title;

![screenshot](/screenshots/netflix-query5.png)

## 6. Specific average rating of movies: A query that takes movie criteria of your choosing and returns a table consisting of title, year, and avg where avg is the average rating received by each movie and meeting some condition of your choosing such as average greater than 4, average less than 3, etc.—the results should be sorted descending by avg (thus listing the top-rated movie first) then ascending by title in case of a tie

Criteria: Returns a table consisting of title, year, and avg rating of movies that contain the name "Star Wars" that have a rating of less than 3, sorted by descending average, ascending title if a tie. (AKA: return the crummy Star Wars titles. Shockkingly The Chistmas Special doesn't appear, likely bc it was never released on DVD).

SELECT title, year, AVG(rating) FROM movie, rating WHERE movie.id = rating.movie_id AND title ILIKE '%Star Wars%' GROUP BY title, year HAVING AVG(rating) < 3 ORDER BY AVG(rating) DESC, title;

![screenshot](/screenshots/netflix-query6.png)


## 7. Number of reviews received by a movie during a certain time period: A query that takes movie criteria of your choosing and returns a table consisting of title, year, and count where count is the number of reviews received by each movie within a particular date range of your choosing such as after 2005, during the month of September, etc.—the results should be sorted descending by count (thus listing the most-frequently-rated movie first) then ascending by title in case of a tie


Criteria: Get the total number of reviews of movies that contained the word "haunt" (to include "haunting," "haunted," etc) somewhere in the title, during "spooky season 2002" (AKA October 2002) and sort by the most reviewed movie, and then title in case of a tie. 

SELECT title, year, COUNT(*) FROM movie, rating WHERE movie.id = rating.movie_id AND title ILIKE '%haunt%' AND date_rated <= '2002-11-01' AND date_rated >= '2002-10-01' GROUP BY title, year ORDER by count DESC, title;

![screenshot](/screenshots/netflix-query7.png)

