
CREATE TABLE IF NOT EXISTS `cms_article_meta`(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `title` VARCHAR(60) NOT NULL,
 `subtitle` VARCHAR(50) NULL,
 `dtpub` TIMESTAMP DEFAULT 0,
 `dtupdate` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 `dtcreate` TIMESTAMP NOT NULL DEFAULT 0,
 `author` VARCHAR(30),
 `source` VARCHAR(30),
 `cover` VARCHAR(200),
 `brief` VARCHAR(255),
 `status` TINYINT(1) DEFAULT 1,
 `cid` int(9) NOT NULL,
 `ctid` int(9) NOT NULL DEFAULT 1,
 PRIMARY KEY(`id`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS cms_article_content(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `content` TEXT DEFAULT NULL,
 PRIMARY KEY(`id`)
)ENGINE=Innodb DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `cms_album`(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `title` VARCHAR(20) NOT NULL,
 `code` VARCHAR(10) UNIQUE NOT NULL,
 `dtcreate` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `remark` VARCHAR(50),
 `status` TINYINT(1) DEFAULT 1,
  PRIMARY KEY(`id`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `cms_album_img`(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `title` VARCHAR(100) NOT NULL,
 `dtcreate` TIMESTAMP NOT NULL DEFAULT 0,
 `file` VARCHAR(255) NOT NULL,
 `aid` int(9) NOT NULL,
 `itype` TINYINT(1) DEFAULT 1,
  PRIMARY KEY(`id`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;


-- user table
CREATE TABLE IF NOT EXISTS `site_user`(
`id` INT(9) NOT NULL AUTO_INCREMENT,
`dtcreate` TIMESTAMP NOT NULL DEFAULT 0,
`email` varchar(60) not null,
`passwd` varchar(64) not null,
`nickname` varchar(50),
`mobile` varchar(20) UNIQUE,
`status` TINYINT(1) DEFAULT 1,
PRIMARY KEY(`id`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `site_user_profile`(
`uid` INT(9) NOT NULL,
`birthday` CHAR(10),
`address` VARCHAR(50),
`remark` VARCHAR(50),
  PRIMARY KEY(`uid`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `site_order`(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `uid` INT(9) NOT NULL,
 `dtcreate` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `dtupdate` TIMESTAMP NOT NULL DEFAULT 0,
 `dtcomplete` TIMESTAMP NOT NULL DEFAULT 0,
 `price` DECIMAL(7,2) DEFAULT 0,
 `remark` VARCHAR(100),
 `title` VARCHAR(50),
 `total_limit` INT(4),
 `edit_limit` INT(4),
 `status` TINYINT(1) DEFAULT 1,
 `venue` VARCHAR(20),
 `dttake` VARCHAR(10),
  PRIMARY KEY(`id`)
)ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `site_order_img`(
 `oid` INT(9) NOT NULL,
 `iid` INT(9) NOT NULL,
 `status` TINYINT(1) DEFAULT 1
)ENGINE=Innodb DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `cms_category`(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `title` VARCHAR(20) NOT NULL,
 `code` VARCHAR(10) UNIQUE NOT NULL,
 `dtcreate` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `remark` VARCHAR(50),
 `status` TINYINT(1) DEFAULT 1,
  PRIMARY KEY(`id`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS cms_article_category(
 `aid` INT(9) NOT NULL,
 `cid` INT(9) NOT NULL
)ENGINE=Innodb DEFAULT CHARSET=utf8;

INSERT INTO `cms_category`(title,code)VALUES('套系报价','txbj');
INSERT INTO `cms_category`(title,code)VALUES('服务流程','fwlc');
INSERT INTO `cms_category`(title,code)VALUES('作品展示','zpzs');
INSERT INTO `cms_category`(title,code)VALUES('摄影学苑','syxy');
INSERT INTO `cms_category`(title,code)VALUES('活动','news');

INSERT INTO `site_order`(uid,price)VALUES(1,999.00);
INSERT INTO `site_order_img`(oid,iid)VALUES(1,1),(1,2),(1,3);

INSERT INTO `cms_album`(`title`,`code`)VALUES('article-common','ac');
INSERT INTO `cms_album`(`title`,`code`)VALUES('home-banner','hb');
INSERT INTO `cms_album`(`title`,`code`)VALUES('home-gallery','hg');
INSERT INTO `cms_album`(`title`,`code`)VALUES('order-all','oa');

CREATE TABLE IF NOT EXISTS `site_preorder`(
 `id` INT(9) NOT NULL AUTO_INCREMENT,
 `utitle` VARCHAR(30) DEFAULT NULL,
 `pdate` CHAR(10),
 `genre` TINYINT(1),
 `age`   TINYINT(2),
 `bdesc` VARCHAR(200),
 `mobile` varchar(20),
 `dtcreate` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `status` TINYINT(1) DEFAULT 1,
 PRIMARY KEY(`id`)
)ENGINE=Innodb DEFAULT CHARSET=utf8;

--alter history
--2016-0513 15:05:15
alter table site_user modify mobile varchar(20) unique;

CREATE TABLE IF NOT EXISTS `site_photographer`(
`id` INT(9) NOT NULL AUTO_INCREMENT,
`dtcreate` TIMESTAMP NOT NULL DEFAULT 0,
`email` varchar(60) not null,
`passwd` varchar(64) not null,
`nickname` varchar(50),
`mobile` varchar(20) UNIQUE,
`status` TINYINT(1) DEFAULT 1,
PRIMARY KEY(`id`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;

alter table site_preorder add pgid INT DEFAULT 1;

CREATE TABLE `shijing_jobs`(
`id` INT(9) NOT NULL AUTO_INCREMENT,
`job_name` VARCHAR(30),
`job_data` VARCHAR(1000),
`job_status` TINYINT(1) DEFAULT 1,
`dtcreate` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
`dtcomplete` TIMESTAMP,
`dtupdate` TIMESTAMP,
`job_result` VARCHAR(100),
PRIMARY KEY(`id`)
)ENGINE=Innodb DEFAULT CHARSET=utf8;

alter TABLE `site_order` add total INT DEFAULT 0;
ALTER TABLE site_order DROP dtcomplete;