
CREATE DATABASE IF NOT EXISTS `shijing_img` DEFAULT CHARACTER SET UTF8 COLLATE utf8_general_ci;
GRANT ALL ON shijing_img.* TO 'imgweb'@'%' IDENTIFIED BY 'shijing09';

CREATE TABLE IF NOT EXISTS `cms_article_meta`(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `title` VARCHAR(60) NOT NULL,
 `subtitle` VARCHAR(50) NOT NULL,
 `dtpub` TIMESTAMP DEFAULT 0,
 `dtupdate` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 `dtcreate` TIMESTAMP NOT NULL DEFAULT 0,
 `author` VARCHAR(30),
 `source` VARCHAR(30),
 `cover` VARCHAR(200),
 `brief` VARCHAR(30),
 `status` TINYINT(1) DEFAULT 1,
 `cid` int(9) NOT NULL,
 PRIMARY KEY(`id`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS cms_article_content(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `content` TEXT DEFAULT NULL,
 PRIMARY KEY(`id`)
)ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS cms_column(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `cname` VARCHAR(20) NOT NULL,
 PRIMARY KEY(`id`)
)ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS cms_article_column(
 `aid` INT(9) NOT NULL,
 `cid` INT(9) NOT NULL
)ENGINE=Innodb DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `cms_album`(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `title` VARCHAR(30) NOT NULL,
 `dtcreate` TIMESTAMP NOT NULL DEFAULT 0,
 `remark` VARCHAR(200),
 `status` TINYINT(1) DEFAULT 1,
  PRIMARY KEY(`id`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `cms_album_img`(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `title` VARCHAR(100) NOT NULL,
 `dtcreate` TIMESTAMP NOT NULL DEFAULT 0,
 `file` VARCHAR(255) NOT NULL,
 `aid` int(9) NOT NULL,
  PRIMARY KEY(`id`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;


-- user table
CREATE TABLE IF NOT EXISTS `site_user`(
`id` INT(9) NOT NULL AUTO_INCREMENT,
`dtcreate` TIMESTAMP NOT NULL DEFAULT 0,
`email` varchar(60) not null,
`passwd` varchar(64) not null,
`nickname` varchar(50),
`cellphone` varchar(20),
`status` TINYINT(1) DEFAULT 1,
PRIMARY KEY(`id`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;
