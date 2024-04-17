-- Check if the database exists, if not create it
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create user hbnb_dev if it does not exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on hbnb_dev_db to hbnb_dev
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilege on performance_schema to hbnb_dev
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
