db schema:

CREATE DATABASE server_config DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL ON server_config.* TO 'sconf'@'%' IDENTIFIED BY 'host321';

DROP TABLE IF EXISTS `sc_config`;
CREATE TABLE `sc_config`(
 lip VARCHAR(15) NOT NULL,
 wip VARCHAR(15) DEFAULT NULL,
 totalmem INT DEFAULT 0,
 cpu SMALLINT DEFAULT 0,
 dt_update TIMESTAMP DEFAULT 0,
 PRIMARY KEY(lip)
 ) ENGINE=INNODB DEFAULT CHARSET=utf8;



