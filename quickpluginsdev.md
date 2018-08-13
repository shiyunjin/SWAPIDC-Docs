# 快速上手-功能插件开发



> 参考功能插件SEO优化编写



### 编写插件的前提：

- 成为[Swap](https://yun.swap.wang/index.php/Dev/)开发者
- 拥有一点[PHP](http://php.net)基础



### 插件文件目录：

文件目录：

```bash
seoyh
├── lang //语言
│   └── Chinese 
│       ├── lang_index.php
│       └── lang_mail.php
├── templates //模版文件
│   └── index.tpl
├── seoyh.php //入口文件
├── seoyh_controller.php //控制器
└── version //插件版本
```

基本组成：

version 插件版本

plugins_controller.php 控制器

plugins.php 入口文件

/lang  语言包

/templates 页面文件



### 插件编写规则：

强制要求：

- 插件目录名为[开发者唯一前缀_插件名] 例如 ftc_seoyh 
- 编写verison文件
- PHP控制器文件头添加 “defined('SWAP_ROOT') or die('非法操作');”

建议：

- 控制器名为 插件名_controller.php 



### 入口文件编写：

样例代码(seoyh.php)

```php
<?php 
defined('SWAP_ROOT') or die('非法操作');
//为了安全起见,请加上这句,否则会报出绝对路径
//---------------------------------插件配置部分--------------------------------------
function seoyh_config(){
$config['swap_plug']='SEO插件'; //插件名
$config['swap_plug_version']='1.0'; //插件版本号
$config['swap_plug_explain']="SEO的插件"; //插件简介
$config['swap_plug_author']='施健';//开发者
$config['swap_plug_website']='http://www.swapidc.com/';//插件官网
return $config;
}
//------------------------------------------------------------------------------------

function seoyh_template(){
	$keyjc=plug_eva('seoyh','关键词');
	$jieshao=plug_eva('seoyh','描述');
	echo '<meta name="keywords" content="'.$keyjc.'" /><meta name="description" content="'.$jieshao.'" />';
}

add_swap_plug('HEAD区域','seoyh_template');

function seoyh_adminlb(&$array){ //插件后台添加配置页面
		$array[]=array('name'=>'SEO设置','link'=>'/index.php/plugin/seoyh/index/');
}

add_swap_plug('管理员菜单列表','seoyh_adminlb');

```

[^Swapidc官方群]: 群文件/SEO优化插件



### 控制器编写：

> ​	找回密码那个写的比较详细 ，所以这里使用找回密码来做案例

样例代码(forgot_password_controller.php)：

```php
<?php
defined('SWAP_ROOT') or die('非法操作');//写上这个就是了
function forgot_password_read() {
	C('MAIL_CHARSET','UTF-8'); //配置
	C('MAIL_HTML',true);
	C('MAIL_ADDRESS',plug_eva('forgot_password','邮箱地址'));
	C('MAIL_SMTP',plug_eva('forgot_password','SMTP服务器地址'));
	C('MAIL_LOGINNAME',plug_eva('forgot_password','邮箱登录帐号'));
	C('MAIL_PASSWORD',plug_eva('forgot_password','邮箱登录密码'));
	C('MAIL_AUTH',true); 
	import("swap.Mail"); //引用邮件发送
}
function forgot_password_randStr($len=6) {
$chars='ABDEFGHJKLMNPQRSTVWXYabdefghijkmnpqrstvwxy23456789';
mt_srand((double)microtime()*1000000*getmypid());
$password='';   
while(strlen($password)<$len)
$password.=substr($chars,(mt_rand()%strlen($chars)),1);   
return $password;   
}
class forgot_password extends controller
{
function config(){ //配置
	return array(
		'swap_no_login' => array(
			'index'=>'1',
			'mail'=>'1'
		),
		'index' => '1',
		'mail'=>'1'
	);
}
function index(){ //页面
	$username=_POST('username');
	if(!empty($username)){
		$this->conn->select('用户','*',"用户名='".$username."' OR 电子邮件='".$username."'");
		if($this->conn->db_num_rows()==0)
			exit(redirect($this->cakurl().'/plugin/forgot_password/index/?error='.$this->lang['不存在的用户名或邮箱']));
		$array=$this->conn->fetch_array();
		$code=forgot_password_randStr();
		forgot_password_read();
		plug_eva('forgot_password','邮件码:'.$code,$array['uid']);
		$lang=plug_lang_get('forgot_password','mail');
		$lang['内容']=str_replace('{<code>}',$code,$lang['内容']);
		SendMail($array['电子邮件'],$lang['标题'],$lang['内容'],$lang['发信人']);
		exit(redirect($this->cakurl().'/plugin/forgot_password/index/?success='.$this->lang['发送找回密码邮件成功,请打开邮箱查看并执行操作']));
	}
	TEMPLATE::display('index.tpl');
}
  
    //验证逻辑
function mail(){
	$code=_POST('code');
	$pass=_POST('pass');
	$repass=_POST('repass');
	if(!empty($code)){
		$uid=plug_eva('forgot_password','邮件码:'.$code);
		if(empty($uid))
			exit(redirect($this->cakurl().'/plugin/forgot_password/mail/?error='.$this->lang['验证码不正确或不存在']));
		if(empty($pass))
			exit(redirect($this->cakurl().'/plugin/forgot_password/mail/?warning='.$this->lang['新密码不得为空']));
		if(!$this->IsUsername($pass))
			exit(redirect($this->cakurl().'/plugin/forgot_password/mail/?warning='.$this->lang['密码格式不正确']));
		if(!$this->IsSame($pass,$repass))
			exit(redirect($this->cakurl().'/plugin/forgot_password/mail/?warning='.$this->lang['2次密码不相同']));
		$this->conn->update('用户',"密码=PASSWORD('".$pass."')","uid='".$uid."'");
		plug_eva('forgot_password','邮件码:'.$code,NULL);
		$this->conn->delete('插件配置',"插件名称='forgot_password' and 值='".$uid."'");
		exit(redirect($this->cakurl().'/index/login/?success='.$this->lang['修改密码成功,请用新密码登入']));
	}
	TEMPLATE::display('mail.tpl');//渲染 视图 
}
}
?>
```



[^Swapidc官方群]: 群文件/找回密码插件



### 管理面板添加配置页面：

​	在后台管理中添加插件配置页面通过调用 add_swap_plug()添加

​	$array[]=array(‘name’=>'[菜单里面内显示名称]例如 "用户清理配置" ', 'link' => '点击后跳转的网友URL 例如 “/index.php/plugin/seoyh/index/” ')



​	link=>跳转链接

​	name=>后台显示链接



```php
function seoyh_adminlb(&$array){ 
		$array[]=array('name'=>'SEO设置','link'=>'/index.php/plugin/seoyh/index/');
} //设置需要添加的内容
add_swap_plug('管理员菜单列表','seoyh_adminlb'); //添加内容
```



### 函数列表：

need_admin(); 需要管理员权限

redirect( url ); 跳转到指定页面

add_swap_plug(); 添加页面

SendMail($array['电子邮件'],$lang['标题'],$lang['内容'],$lang['发信人']); 发送邮件

C(); 对某些参数进行动态配置





### add_swap_plug();

> 非常重要

食用方法：

```php
add_swap_plug(’位置‘,'function')
//例如：
add_swap_plug('登入页底部','forgot_password_template');
```



### redirect();

 跳转到指定页面

```php
redirect("https://www.google.com");//重定向到 www.google.com
```



### need_admin();

需要管理员才可以运行

```php
need_admin();
```



### SendMail();

需 “import("swap.Mail");”

发送邮件：

```php
import("swap.Mail");
SendMail(电子邮件,标题,内容,发信人);
//例如：
SendMail('swap@user.com','邮件的标题，这是一封可爱的邮件','邮件的内容，嘤嘤嘤，嘤嘤嘤','嘤嘤怪Franary')
```



### C():

在具体的Action方法里面，可以用C()对某些参数进行动态配置，主要指那些还没有使用的参数。

具体用法如下：

 C('参数名称'); 获取已经设置的参数值

 C('参数名称','新的参数值'); 设置新的值



样例代码(forgot_password_controller.php)：

```PHP
function forgot_password_read() {
	C('MAIL_CHARSET','UTF-8');
	C('MAIL_HTML',true);
	C('MAIL_ADDRESS',plug_eva('forgot_password','邮箱地址'));
	C('MAIL_SMTP',plug_eva('forgot_password','SMTP服务器地址'));
	C('MAIL_LOGINNAME',plug_eva('forgot_password','邮箱登录帐号'));
	C('MAIL_PASSWORD',plug_eva('forgot_password','邮箱登录密码'));
	C('MAIL_AUTH',true);
	import("swap.Mail");
}
```



### plug_lang_get();

使用语言 /lang/目录下语言包

样例

```php
$lang=plug_lang_get('forgot_password','mail');
```



### TEMPLATE::display();

渲染页面或使用/templates/"页面.tpl"

样例

```php
TEMPLATE::display('index.tpl');
```



### plug_eva();

...待补充