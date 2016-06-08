CREATE DATABASE IF NOT EXISTS dkdbprojects;

CREATE TABLE dkdbprojects.section_points (
    point_id BIGINT AUTO_INCREMENT, 
	lat DOUBLE NULL, 
	lon DOUBLE NULL,
	PRIMARY KEY(point_id)
);

CREATE TABLE dkdbprojects.road_sections (
	section_id   BIGINT AUTO_INCREMENT, 
	start_point  BIGINT NULL, 
	end_point    BIGINT NULL, 
	section_type TINYINT UNSIGNED NULL, 
	PRIMARY KEY (section_id),
	FOREIGN KEY (start_point) REFERENCES  dkdbprojects.section_points(point_id),
	FOREIGN KEY (end_point)   REFERENCES  dkdbprojects.section_points(point_id)
);

CREATE TABLE dkdbprojects.defects (
	defect_id BIGINT AUTO_INCREMENT, 
	lat DOUBLE NULL, 
	lon DOUBLE NULL,
	direction DOUBLE NULL,
	defect_type TINYINT UNSIGNED NULL, 
	section_id BIGINT, 
	PRIMARY KEY(defect_id),
	FOREIGN KEY (section_id)   REFERENCES  dkdbprojects.road_sections(section_id)
);

INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.318877", "44.026066");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.318145", "44.023137");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.317001", "44.019366");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.316037", "44.016083");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.315019", "44.012660");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.313936", "44.009720");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.312895", "44.006673");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.311870", "44.003652");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.310552", "43.999656");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.309601", "43.995767");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.308786", "43.991551");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.308036", "43.987957");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.308232", "43.985607");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.309934", "43.986712");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.311404", "43.988268");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.312791", "43.989834");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.313797", "43.993256");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.314434", "43.996389");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.315083", "43.999715");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.315743", "44.003416");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.316481", "44.006838");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.317278", "44.011183");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.317927", "44.014273");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.318641", "44.015357");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.319986", "44.013930");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.320926", "44.012857");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.322574", "44.010947");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.323460", "44.009971");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.324150", "44.009134");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.324584", "44.008705");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.326012", "44.006978");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.326815", "44.006066");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.328992", "44.008695");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.328700", "44.012214");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.328337", "44.015840");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.327843", "44.017900");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.326695", "44.022041");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.325779", "44.025549");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.325194", "44.027732");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.324224", "44.031627");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.323427", "44.034256");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.322487", "44.034921");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.321868", "44.038150");
INSERT INTO dkdbprojects.section_points (lat, lon) VALUES ("56.321261", "44.042366");

INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (1, 2, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (2, 3, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (3, 4, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (4, 5, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (5, 6, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (6, 7, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (7, 8, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (8, 9, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (9, 10, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (10, 11, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (11, 12, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (12, 13, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (13, 14, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (14, 15, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (15, 16, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (16, 17, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (17, 18, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (18, 19, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (19, 20, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (20, 21, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (21, 22, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (22, 23, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (23, 24, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (24, 25, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (25, 26, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (26, 27, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (27, 28, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (28, 29, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (29, 30, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (30, 31, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (31, 32, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (32, 33, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (33, 34, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (34, 35, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (35, 36, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (36, 37, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (37, 38, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (38, 39, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (39, 40, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (40, 41, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (41, 42, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (42, 43, 1);
INSERT INTO dkdbprojects.road_sections (start_point, end_point, section_type) VALUES (43, 44, 1);

