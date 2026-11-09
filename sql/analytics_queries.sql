-- 1. Competitions with category
SELECT c.competition_name, a.category_name, c.type, c.gender FROM competitions c
LEFT JOIN categories a ON a.category_id=c.category_id;
-- 2. Competition count per category
SELECT a.category_name, COUNT(c.competition_id) total FROM categories a
LEFT JOIN competitions c ON c.category_id=a.category_id GROUP BY a.category_name;
-- 3. Doubles competitions
SELECT * FROM competitions WHERE type='doubles';
-- 4. Competitions in ITF Men (adjust to exact category label returned by API)
SELECT c.* FROM competitions c JOIN categories a ON a.category_id=c.category_id WHERE a.category_name='ITF Men';
-- 5. Parent and child competitions
SELECT p.competition_name parent, ch.competition_name child FROM competitions ch
JOIN competitions p ON ch.parent_id=p.competition_id;
-- 6. Competition type distribution
SELECT a.category_name,c.type,COUNT(*) total FROM competitions c
LEFT JOIN categories a ON a.category_id=c.category_id GROUP BY a.category_name,c.type;
-- 7. Top-level competitions
SELECT * FROM competitions WHERE parent_id IS NULL;
-- 8. Venues with complex
SELECT v.venue_name,x.complex_name FROM venues v JOIN complexes x ON x.complex_id=v.complex_id;
-- 9. Venue count by complex
SELECT x.complex_name,COUNT(v.venue_id) venue_count FROM complexes x
LEFT JOIN venues v ON v.complex_id=x.complex_id GROUP BY x.complex_name;
-- 10. Venues in Chile
SELECT * FROM venues WHERE country_name='Chile';
-- 11. Venue timezones
SELECT venue_name,city_name,country_name,timezone FROM venues;
-- 12. Complexes with multiple venues
SELECT x.complex_name,COUNT(*) venue_count FROM complexes x JOIN venues v ON v.complex_id=x.complex_id
GROUP BY x.complex_name HAVING COUNT(*)>1;
-- 13. Venues grouped by country
SELECT country_name,COUNT(*) venue_count FROM venues GROUP BY country_name ORDER BY venue_count DESC;
-- 14. Venues in complex Nacional
SELECT v.* FROM venues v JOIN complexes x ON x.complex_id=v.complex_id WHERE x.complex_name LIKE '%Nacional%';
-- 15. Competitors with rank and points
SELECT p.name,p.country,r.rank,r.points,r.movement,r.competitions_played FROM competitors p
JOIN competitor_rankings r ON r.competitor_id=p.competitor_id ORDER BY r.rank;
-- 16. Top five competitors
SELECT p.name,r.rank,r.points FROM competitors p JOIN competitor_rankings r
ON r.competitor_id=p.competitor_id WHERE r.rank<=5 ORDER BY r.rank;
-- 17. Stable rank
SELECT p.name,r.rank,r.movement FROM competitors p JOIN competitor_rankings r
ON r.competitor_id=p.competitor_id WHERE r.movement=0;
-- 18. Points total for Croatia
SELECT p.country,SUM(r.points) total_points FROM competitors p JOIN competitor_rankings r
ON r.competitor_id=p.competitor_id WHERE p.country='Croatia' GROUP BY p.country;
-- 19. Competitors per country
SELECT country,COUNT(*) competitor_count FROM competitors GROUP BY country ORDER BY competitor_count DESC;
-- 20. Highest points in stored snapshot
SELECT p.name,p.country,r.points,r.rank FROM competitors p JOIN competitor_rankings r
ON r.competitor_id=p.competitor_id WHERE r.points=(SELECT MAX(points) FROM competitor_rankings);
