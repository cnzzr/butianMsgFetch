# 补天平台排名和消息自动提醒

## 功能说明
该脚本实现从补丁平台的系统消息、极客空间中抓取关键信息再通过微信通知给“白帽子”，减少手工操作。
提醒功能依赖于微信公众号（需要自行申请开通） 或者 使用第三方 推送精灵

![提醒效果](https://shs3.b.qianxin.com/butian_public/f7526627a522cba1146ecc3a4ded0659e91b70298bf55.png)

## 配置说明
1、修改配置文件
	butian.cfg.template 为配置文件模板
	修改配置文件将cookie的值修改为您登录补丁后获取的cookie值，有效期为7天，过期后将提醒更新。
2、找到电脑创建计划任务，每半小时执行一次

## 开发计划
V2：利用强化学习算法对配置的域名自动挖洞提交
V3：取消配置文件，通过脑波记录使用者的想法自动挖洞提交
V5：自动监测发布测试任务，自动添加任务进行自动挖洞，有情况邮件提醒
V6：一键干掉审核，越权审核漏洞
V7：让审核心软
V8：一键获得平台所有权
v9：自动打款
v10：让ceo转让股份
……
v666：破灭世间一切苦
