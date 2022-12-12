select cust.customer_id,
      cust.firstname,
      cust.lastname,
      cust.birthdate,
      cust.residence_city_id,
      cust.notice_city_id,
      residence_city.name as residence_city_name,
      notice_city.name as notice_city_name
from customer cust
join city residence_city
on cust.residence_city_id=residence_city.city_id
join city notice_city
on cust.notice_city_id=notice_city.city_id;

select cust.customer_id,
      cust.firstname,
      cust.lastname,
      cust.birthdate,
      cust.residence_city_id,
      cust.notice_city_id,
      residence_city.name as residence_city_name,
      notice_city.name as notice_city_name
from customer cust
join city residence_city
on cust.residence_city_id=residence_city.city_id
join city notice_city
on cust.notice_city_id=notice_city.city_id;

SELECT game.game_date_est, 
    game.game.id, 
    game.nickname, 
    game.team.id, 
    game.home_team_id, 
    game.visitor_team_id, 
    game.pts_home, 
    game.pts_away
FROM game INNER JOIN team 
ON game.home_team_id = team.id
WHERE game.id = 21800013



SELECT gam.game_date_est, gam.game.id, gam.nickname, gam.team.id, gam.home_team_id, gam.visitor_team_id, gam.pts_home, gam.pts_away, home_team.nickname as home_team, visitor_team.nickname as away_team
FROM game gam 
JOIN team home_team
ON gam.home_team_id=home_team.id
JOIN team away_team
ON gam.visitor_team_id=away_team.id
WHERE game.id = 21800013;


SELECT gam.game_date_est, 
    gam.id, 
    gam.home_team_id, 
    gam.visitor_team_id, 
    gam.pts_home, 
    gam.pts_away,
    home_team.nickname as home_team,
    visitor_team.nickname as visitor_team
FROM game gam 
JOIN team home_team
ON gam.home_team_id=home_team.id
JOIN team visitor_team
ON gam.visitor_team_id=visitor_team.id
WHERE gam.id = 21800013;