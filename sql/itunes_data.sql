-- itunes_data definition
CREATE TABLE itunes_data (
	persistent_id varchar(100) PRIMARY KEY,
	track_id integer,
	track_name text,
	artist text,
	album_artist text,
	album text,
	genre varchar(100),
	disc_number smallint,
	disc_count smallint,
	track_number smallint,
	track_count smallint,
	album_year date,
	date_modified timestamp,
	date_added timestamp,
	volume_adjustment smallint,
	play_count integer,
	play_date_utc timestamp,
	artwork_count smallint,
	md5_id varchar(100)
);

-- itunes_data_tmp definition
CREATE TABLE itunes_data_tmp (
	persistent_id varchar(100),
	track_id integer,
	track_name text,
	artist text,
	album_artist text,
	album text,
	genre varchar(100),
	disc_number smallint,
	disc_count smallint,
	track_number smallint,
	track_count smallint,
	album_year date,
	date_modified timestamp,
	date_added timestamp,
	volume_adjustment smallint,
	play_count integer,
	play_date_utc timestamp,
	artwork_count smallint,
	md5_id varchar(100)
);

-- itunes_data_log definition
CREATE TABLE itunes_data_log (
	persistent_id varchar(100) references itunes_data(persistent_id),
	track_id integer,
	track_name text,
	artist text,
	album_artist text,
	album text,
	genre varchar(100),
	disc_number smallint,
	disc_count smallint,
	track_number smallint,
	track_count smallint,
	album_year date,
	date_modified timestamp,
	date_added timestamp,
	volume_adjustment smallint,
	play_count integer,
	play_date_utc timestamp,
	artwork_count smallint,
	md5_id varchar(100)
);

SELECT EXISTS (SELECT 1 from itunes_data_tmp idt);
DELETE FROM itunes_data_tmp;
DELETE FROM itunes_data;


-- TRIGGERS (3)
-- (1) UPDATES itunes_data if insertion in itunes_data_tmp shows changes
-- also LOGS this change in itunes_data_log
CREATE TRIGGER IF NOT EXISTS tr_insert_itunes_data_tmp AFTER INSERT ON itunes_data_tmp
BEGIN
	INSERT INTO itunes_data_log (
		persistent_id, 
		track_id,
		track_name,
		artist,
		album_artist,
		album, genre,
		disc_number,
  		disc_count,
		track_number,
		track_count,
		album_year,
		date_modified,
		date_added,
		volume_adjustment,
		play_count,
  		play_date_utc,
		artwork_count,
		md5_id)
  	SELECT
		NEW.persistent_id,
		NEW.track_id, NEW."name", NEW.artist, NEW.album_artist, NEW.album, NEW.genre, NEW.disc_number,
  		NEW.disc_count, NEW.track_number, NEW.track_count, NEW."year", NEW.date_modified, NEW.date_added, NEW.volume_adjustment,
  		NEW.play_count,	NEW.play_date_utc, NEW.artwork_count, NEW.md5_id
  	FROM itunes_data id
  	WHERE persistent_id = NEW.persistent_id AND (
  		track_id IS NOT NEW.track_id
  		OR "name" IS NOT NEW."name"
 		OR artist IS NOT NEW.artist
 		OR album_artist IS NOT NEW.album_artist
 		OR album IS NOT NEW.album
 		OR genre IS NOT NEW.genre
 		OR disc_number IS NOT NEW.disc_number
 		OR disc_count IS NOT NEW.disc_count
 		OR track_number IS NOT NEW.track_number
 		OR track_count IS NOT NEW.track_count
 		OR "year" IS NOT NEW."year"
 		OR date_modified IS NOT NEW.date_modified
 		OR date_added IS NOT NEW.date_added
 		OR volume_adjustment IS NOT NEW.volume_adjustment
 		OR play_count IS NOT NEW.play_count
 		OR play_date_utc IS NOT NEW.play_date_utc
 		OR artwork_count IS NOT NEW.artwork_count
		OR md5_id IS NOT NEW.md5_id
	);
	
	UPDATE itunes_data 
  		SET track_id = NEW.track_id,
  			name = NEW.name,
  			artist = NEW.artist,
  			album_artist = NEW.album_artist,
  			album = NEW.album,
  			genre = NEW.genre,
  			disc_number = NEW.disc_number,
  			disc_count = NEW.disc_count,
  			track_number = NEW.track_number,
  			track_count = NEW.track_count,
  			"year" = NEW."year",
  			date_modified = NEW.date_modified,
  			date_added = NEW.date_added,
  			volume_adjustment = NEW.volume_adjustment,
  			play_count = NEW.play_count,
  			play_date_utc = NEW.play_date_utc,
  			artwork_count = NEW.artwork_count,
  			md5_id = NEW.md5_id
 		WHERE persistent_id = NEW.persistent_id AND (
 			track_id IS NOT NEW.track_id
  			OR name IS NOT NEW.name
 			OR artist IS NOT NEW.artist
 			OR album_artist IS NOT NEW.album_artist
 			OR album IS NOT NEW.album
 			OR genre IS NOT NEW.genre
 			OR disc_number IS NOT NEW.disc_number
 			OR disc_count IS NOT NEW.disc_count
 			OR track_number IS NOT NEW.track_number
 			OR track_count IS NOT NEW.track_count
 			OR "year" IS NOT NEW."year"
 			OR date_modified IS NOT NEW.date_modified
 			OR date_added IS NOT NEW.date_added
 			OR volume_adjustment IS NOT NEW.volume_adjustment
 			OR play_count IS NOT NEW.play_count
 			OR play_date_utc IS NOT NEW.play_date_utc
 			OR artwork_count IS NOT NEW.artwork_count
			OR md5_id IS NOT NEW.md5_id
	);
END;
 
-- (2) Log deletions from itunes_data
CREATE TRIGGER IF NOT EXISTS tr_delete_itunes_data BEFORE DELETE ON itunes_data
BEGIN
    INSERT INTO itunes_data_log (persistent_id, track_id, "name", artist, album_artist, album, genre, disc_number,
  		disc_count, track_number, track_count, "year", date_modified, date_added, volume_adjustment, play_count,
  		play_date_utc, artwork_count, md5_id)
    SELECT persistent_id, track_id, "name", artist, album_artist, album, genre, disc_number,
  		disc_count, track_number, track_count, "year", date_modified, date_added, volume_adjustment, play_count,
  		play_date_utc, artwork_count, md5_id
    FROM itunes_data
    WHERE persistent_id = OLD.persistent_id;
END;


-- -------------------------
-- POSTGRES SPECIFIC LOGGING
-- --------------------------
CREATE TABLE IF NOT EXISTS itunes_data_audit_log (
    persistent_id varchar(100) NOT NULL,
    old_row_data jsonb,
    new_row_data jsonb,
    dml_type dml_type NOT NULL,
    dml_timestamp timestamp NOT NULL,
    PRIMARY KEY (persistent_id, dml_type, dml_timestamp)
);

CREATE TYPE dml_type AS ENUM ('INSERT', 'UPDATE', 'DELETE');