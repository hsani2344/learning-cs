-- SQL query to list the titles of all movies in which both Bradley Cooper and Jennifer Lawrence starred
SELECT title
  FROM movies
 WHERE id IN
       (SELECT movie_id
          FROM stars
          JOIN people
            ON people.id = stars.person_id
         WHERE people.name = 'Bradley Cooper')
   AND id IN
       (SELECT movie_id
          FROM stars
          JOIN people
            ON people.id = stars.person_id
         WHERE people.name = 'Jennifer Lawrence');
