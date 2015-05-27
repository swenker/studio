CREATE DATABASE IF NOT EXISTS `shijing_img` DEFAULT CHARACTER SET UTF8 COLLATE utf8_general_ci;
GRANT ALL ON shijing_img.* TO 'imgweb'@'%' IDENTIFIED BY 'shijing09';
GRANT ALL ON shijing_img.* TO 'imgweb'@'localhost' IDENTIFIED BY 'shijing09';



CREATE DATABASE IF NOT EXISTS `shijing_img_test` DEFAULT CHARACTER SET UTF8 COLLATE utf8_general_ci;
GRANT ALL ON shijing_img_test.* TO 'imgweb'@'%' IDENTIFIED BY 'shijing09';
GRANT ALL ON shijing_img_test.* TO 'imgweb'@'localhost' IDENTIFIED BY 'shijing09';
