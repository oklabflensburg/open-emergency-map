-- POSTGIS ERWEITERUNG LADEN
CREATE EXTENSION IF NOT EXISTS postgis;


-- TABELLE POLIZEIDIENSTSTELLEN SCHLESWIG-HOLSTEIN
DROP TABLE IF EXISTS sh_police_station CASCADE;

CREATE TABLE IF NOT EXISTS sh_police_station (
  id INT NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  city VARCHAR(255) NOT NULL,
  zipcode VARCHAR(5) NOT NULL,
  street VARCHAR(255) NOT NULL,
  house_number VARCHAR(10),
  telephone VARCHAR,
  fax VARCHAR,
  email VARCHAR,
  website VARCHAR,
  longitude DECIMAL(9, 6),
  latitude DECIMAL(8, 6),
  wkb_geometry GEOMETRY(GEOMETRY, 4326)
);

CREATE INDEX IF NOT EXISTS sh_police_station_wkb_geometry_idx ON sh_police_station USING GIST (wkb_geometry);
