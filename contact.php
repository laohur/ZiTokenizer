<meta http-equiv="Content-type" content="script/php;charset=utf-8">
<?php
//保存图片文件
@header('Content-type: text/html;charset=UTF-8');<!-- 声明编码 -->

//上传图片
$filepath=$_FILES["photo"]["tmp_name"];
$filename=explode('.',$_FILES['photo']['name']);
$filename[0]=$_POST['name'];
$name=implode('.',$filename);

$uploaded="./photos/".$name;
if(file_exists($filepath)){
	move_uploaded_file($filepath,$uploaded);
	//图片链接插入数据库,方便点击和下载查看,没必要吧图片本身上传到数据库,编码还解码,
	$_POST['photo']="http://localhost/1/c/photos/".$name;
	echo "<br>hello,<br>".$_POST["name"]."!<br><img src='".$uploaded."' <p>";//返回成功信息,而且是自己的头像

}

<!-- 这个字符串是最初开始有的,设计时键入的. 然后在后面以数组形式插入数据库时,中间经过了很多次在test.php上实验,从$arr到$arr5,中间不停滴var_dump($arr),最终挑了一个.没必要吧处理脚本笑出来.我费了好大劲,发现太麻烦了,而这也是一个中间件过程,没必要,只要有结果就好,本地手动处理完毕就好,中间怎么处理的,办法就很多了 -->

$arr1="name,nickname,gender,birthday,phone,qq,email,home,college,grade,major,company,position,address,weibolink,renrenlink,qqzonelink,photo,profile";

//没想好怎么防止sql注入,就用pdo_prepare

$db=new PDO("mysql:host=localhost;dbname=test","root","") or die(print_r($db->errorInfo(),true));

//下面是尝试的代码,因为mysql乱码,试了下这个,最终不行.只好换了mariadb,整个世界就清净了.可以删掉,用以参考.
    mysqli_query("set names ’utf8’ "); 
    mysqli_query("set character_set_client=utf8"); 
    mysqli_query("set character_set_results=utf8"); 

//这是唯一一个自动处理脚本,最初想着把运算都放在这里其实这个是变量静态的,被当地处理完毕再放上来未尝不可,因为简单,实现了,本地把 '?'.'?,'*18 的结果贴出来就可以了.
$s="?";
for($j=0;$j<18;$j++){
	$s.=",?";
}

$add="insert into contact ({$arr1}) values ({$s})";
$q=$stmt=$db->prepare($add);

//这个就是本地吧文本处理完毕再放上来,看着很难输入,中间也出错了很多次,

$array=array($_POST["name"],$_POST["nickname"],$_POST["gender"],$_POST["birthday"],$_POST["phone"],$_POST["qq"],$_POST["email"],$_POST["home"],$_POST["college"],$_POST["grade"],$_POST["major"],$_POST["company"],$_POST["position"],$_POST["address"],$_POST["weibolink"],$_POST["renrenlink"],$_POST["qqzonelink"],$_POST["photo"],$_POST["profile"]);
$stmt->execute($array);

?>

<!-- laohur@gmail.com方便联系 -->