



<h1 align="center">
  青龙安装Bot监控
  <br>
</h1>

## 1.进入青龙容器内

``` bash
# 进入青龙容器内，“ql” 为容器名字，根据自己的容器名修改
docker exec -it ql /bin/bash
```

## 2.一键安装

``` shell
rm -f install.sh* && wget -q https://raw.githubusercontent.com/mrright-cyber/gd/main/install.sh && bash install.sh
```

## 3.配置 TG 机器人参数

* [x] `bot.json`  填写你的机器人 token 用户id等参数
* [x] `diybotset.json` 填写监控群组频道id等参数
* [x] `jk.json` 自定义监控变量和应对脚本路径

## 4.启动机器人

```bash
# 进入对应目录
cd /ql/jbot/

# 第一次启动是这样启动，后续启动参考底部相关命令
pm2 start ecosystem.config.js 
# 查看 jbot 运行状态
pm2 status jbot 

# 查看日志
tail -100f /ql/log/bot/run.log

```

​											

- [x] 如TG收到机器人信息，证明你填写的机器人参数是正确的。

![图2：完成登录，tg机器人发通知](https://raw.githubusercontent.com/curtinlv/gd/main/img/p2.png)

## **登录user开启监控**

- [x] a.发送【/user】 点击 **“重新登录”**

![图1：首次登录授权个人tg](https://raw.githubusercontent.com/curtinlv/gd/main/img/p5.png)

- [x] b.输入手机号格式0086x x xx x x (要关闭两步验证)

![图2：登录](https://raw.githubusercontent.com/curtinlv/gd/main/img/p7.png)

- [x] c.发送【user?】 给你的机器人，有以下回复，证明监控状态正常。

![图3：测试1](https://raw.githubusercontent.com/curtinlv/gd/main/img/p8.png)

![图4：测试2](https://raw.githubusercontent.com/curtinlv/gd/main/img/p9.png)

- [x] 在所监控的频道发出变量，机器人会马上通知：

![图4：测试2](https://raw.githubusercontent.com/curtinlv/gd/main/img/p4.png)



<h1 align="center">
  恭喜你，部署已完成。
  <br>
</h1>


```bash
#################### 相关命令 ####################
操作环境：进入容器内
## 查看机器人运行状态
pm2 status jbot

## 启动机器人：
pm2 start jbot

## 停止机器人
pm2 stop jbot

## 重启机器人
pm2 restart jbot

## 一键更新1
rm -rf /ql/repo/gd && cd /ql/repo/ && git clone https://github.com/mrright-cyber/gd.git && pm2 stop jbot ; rm -rf /ql/jbot/* && cp -a /ql/repo/gd/* /ql/jbot/ ; pm2 start jbot

#或一键更新2
if [ -d /ql/data ];then QL=/ql/data;else QL=/ql; fi;cd ${QL} && rm -f update.sh* && wget  -q https://raw.githubusercontent.com/mrright-cyber/gd/main/update.sh >/dev/null && bash update.sh

## 卸载机器人
pm2 stop jbot && pm2 delete jbot
rm -rf /ql/jbot/*
rm -rf /ql/data/jbot/*

```



## 机器人指令

`/restart` 重启机器人

`/upgd` 更新机器人

`/user?` 查看监控状态

`/clean` 清理缓存日志，释放空间

`/help` 命令帮助
