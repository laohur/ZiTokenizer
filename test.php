<!-- 
contact.html 用于显示和填写表单
contact.php用于处理表单
test.php 用于调试,中间处理.  以及说明

html.javascript.css因为各自表现不同而分开,各自负责内容,动态,美观.
mvc也一样,model负责数据处理,数据库,view负责展示,config负责把他们组织起来.

contact.html和contact.php分工也一样,一个输入表单,一个处理



环境:用xmpp或者lamp,adminer.phpmyadmin和mysql不好支持utf8,改为mariadb和adminer.
adminer可视化建表.用它导出来语句是

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


将上文粘贴到adminer,sql语句执行.排序用utf8_unicode_ci.mysql怎么弄也是乱码,phpmyadmin也是,只好换掉.

按照https://downloads.mariadb.org/mariadb/repositories/#distro=Debian&distro_release=wheezy&version=10.0&mirror=yamagata-university 把mysql换成mariadb,数据不变.
adminer更简单,也安全.下载adminer.php放上去就可以了.

sudo apt-get install python-software-properties sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db sudo add-apt-repository 'deb http://ftp.yz.yamagata-u.ac.jp/pub/dbms/mariadb/repo/10.0/debian wheezy main'

Once the key is imported and the repository added you can install MariaDB with:

sudo apt-get update sudo apt-get install mariadb-server

在test.php中调试时,每一个变量前后都使用了

echo "<br>".'$arr:'."<br>";
var_dump($arr2);

类似的语句

还有一些字符串处理等中间工作也是在这里完成的.
中间处理在本地处理好之后把结果放上去就好了,不用上传过程.

这里每一句都花了不少的心血.

独立程序,编写时不会的上网查函数,不要抄袭已有成果.

-->



<?php


$arr1="name,nickname,gender,birthday,phone,qq,email,home,college,grade,major,company,position,address,weibolink,renrenlink,qqzonelink,profile";

$arr2=explode(",",$arr1);
echo "<br>".'$arr2'."<br>";

for($i=0;$i<count($arr2);$i++){
	$arr3[$i]='"$_POST[\''.$arr2[$i].'\']"';
}
echo "<br>".'$arr3'."<br>";
echo $arr3;
$arr4=implode(",",$arr3);
//'$_POST['name']','$_POST['nickname']','$_POST['gender']','$_POST['birthday']','$_POST['phone']','$_POST['qq']','$_POST['email']','$_POST['home']',........
echo "<br>".'$arr4'."<br>";
echo $arr4;
$arr5="'".$arr4."'";
echo "<br>".'$arr5'."<br>";
echo $arr5;

$db=new PDO("mysql:host=localhost;dbname=test","root","");
//$r1=$db->exec("insert into contact(name,nickname,gender,birthday,phone,qq,email,home,college,grade,major,company,position,address,weibolink,renrenlink,qqzonelink,profile) values ($arr3)");
echo '$db:';

$insert="insert into contact({$arr1}) values ({$arr4})";
echo "<br>".'$insert:'."<br>";


$s="?";
for($j=0;$j<18;$j++){
	$s.=",?";
}

$add="insert into contact ({$arr1}) values ($s)";
$stmt=$db->prepare($add);
$stmt->execute(array($arr4));

?>

$sql = " insert into `tbl` values(' " . $_POST['name'] .  " ', ' " . $_POST['title'] . " ' )";
$sql = " insert into `tbl` values('{$_POST['name']}', '{$_POST['title']}')"

'INSERT INTO '.$table.' ('.$cols.') VALUES ('.$vals.')');

$stmt = $dbh->prepare("SELECT * FROM REGISTRY where name = ?");
if ($stmt->execute(array($_GET['name']))) {
  while ($row = $stmt->fetch()) {
    print_r($row);
  }
}

$array=("{$_POST['name']}","{$_POST['nickname']}","{$_POST['gender']}","{$_POST['birthday']}","{$_POST['phone']}","{$_POST['qq']}","{$_POST['email']}","{$_POST['home']}","{$_POST['college']}","{$_POST['grade']}","{$_POST['major']}","{$_POST['company']}","{$_POST['position']}","{$_POST['address']}","{$_POST['weibolink']}","{$_POST['renrenlink']}","{$_POST['qqzonelink']}","{$_POST['profile']}");

"$_POST['name']","$_POST['nickname']","$_POST['gender']","$_POST['birthday']","$_POST['phone']","$_POST['qq']","$_POST['email']","$_POST['home']","$_POST['college']","$_POST['grade']","$_POST['major']","$_POST['company']","$_POST['position']","$_POST['address']","$_POST['weibolink']","$_POST['renrenlink']","$_POST['qqzonelink']","$_POST['profile']"
$arr5
'"$_POST['name']","$_POST['nickname']","$_POST['gender']","$_POST['birthday']","$_POST['phone']","$_POST['qq']","$_POST['email']","$_POST['home']","$_POST['college']","$_POST['grade']","$_POST['major']","$_POST['company']","$_POST['position']","$_POST['address']","$_POST['weibolink']","$_POST['renrenlink']","$_POST['qqzonelink']","$_POST['profile']"'$db:
$insert:

<!-- laohur@gmail.com谨防联系 -->