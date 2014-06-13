
<p><a href="http://6user.com/0/c/gr/">通讯录</a> 非常简洁的通讯录搜集程序,用文件管理上传的图片.</p>
	连接搜集整理联系信息非常麻烦,就制作了这样一个程序,包括一个html和php,使用时改下数据库,自动生成数据表,把链接分发出去,就能搜集通讯录了,非常简便.除了图片拖拽上传,其他表单元素都用了html5,成功的话返回用户名和图片.<p>
	contact.html 用于显示和填写表单
contact.php用于处理表单
test.php 用于调试,中间处理.以及说明.

html.javascript.css因为各自表现不同而分开,各自负责内容,动态,美观.
mvc也一样,model负责数据处理,数据库,view负责展示,config负责把他们组织起来.

contact.html和contact.php分工也一样,一个输入表单,一个处理



环境:用xmpp或者lamp,adminer.phpmyadmin和mysql不好支持utf8,改为mariadb和adminer.
adminer可视化建表.用它导出来语句是<p>

SET NAMES utf8;
SET foreign_key_checks = 0;
SET time_zone = '+00:00';
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `contact`;
CREATE TABLE `contact` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `nickname` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `gender` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `birthday` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone` int(20) DEFAULT NULL,
  `qq` int(20) DEFAULT NULL,
  `email` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `home` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `college` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `grade` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `major` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `company` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `position` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `address` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `weibolink` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `renrenlink` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `qqzonelink` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `photo` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `profile` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


将上文粘贴到adminer,sql语句执行.排序用utf8_unicode_ci.


