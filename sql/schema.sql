CREATE TABLE categories (category_id VARCHAR(50) PRIMARY KEY, category_name VARCHAR(100) NOT NULL);
CREATE TABLE competitions (
 competition_id VARCHAR(50) PRIMARY KEY, competition_name VARCHAR(150) NOT NULL,
 parent_id VARCHAR(50) NULL, type VARCHAR(30) NOT NULL, gender VARCHAR(20) NOT NULL,
 level VARCHAR(50), category_id VARCHAR(50),
 FOREIGN KEY(category_id) REFERENCES categories(category_id),
 INDEX idx_comp_category(category_id), INDEX idx_comp_parent(parent_id), INDEX idx_comp_type(type)
);
CREATE TABLE complexes (complex_id VARCHAR(50) PRIMARY KEY, complex_name VARCHAR(150) NOT NULL);
CREATE TABLE venues (
 venue_id VARCHAR(50) PRIMARY KEY, venue_name VARCHAR(150) NOT NULL,
 city_name VARCHAR(100) NOT NULL, country_name VARCHAR(100) NOT NULL,
 country_code CHAR(3), timezone VARCHAR(100) NOT NULL, complex_id VARCHAR(50) NOT NULL,
 FOREIGN KEY(complex_id) REFERENCES complexes(complex_id), INDEX idx_venue_country(country_name)
);
CREATE TABLE competitors (
 competitor_id VARCHAR(50) PRIMARY KEY, name VARCHAR(150) NOT NULL,
 country VARCHAR(100) NOT NULL, country_code CHAR(3), abbreviation VARCHAR(20),
 INDEX idx_comp_country(country)
);
CREATE TABLE competitor_rankings (
 rank_id INT AUTO_INCREMENT PRIMARY KEY, rank INT NOT NULL, movement INT NOT NULL DEFAULT 0,
 points INT NOT NULL DEFAULT 0, competitions_played INT NOT NULL DEFAULT 0,
 competitor_id VARCHAR(50) NOT NULL, ranking_type VARCHAR(30) NOT NULL DEFAULT 'doubles',
 fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(competitor_id) REFERENCES competitors(competitor_id),
 UNIQUE KEY uq_rank_player_type(rank,competitor_id,ranking_type),
 INDEX idx_rank_points(points), INDEX idx_rank_rank(rank)
);
