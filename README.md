# 弹幕🐓🐓🐓
> 用来看b站直播时的弹幕用的

## 介绍
使用websocket，没有那种louB的反复http请求奥，就这

## 目前进度：
- 支持查看弹幕消息和送礼物消息

## 画饼：
- 打算配合图形界面，实现美观实用功能（画了一半了 奥利给）
- 整合点歌鸡功能，可以查看目前正在播放的音乐（外部播放器），也可以根据弹幕内容实现歌曲点播
- 有能力的话，实现在图形界面中发送弹幕到直播间，而不用单独打开直播间回复弹幕消息（针对哑巴主播比如我）

## 更新说明
- 2020.5.6
> +使用websocket建立与b站直播服务器的连接，可接收到弹幕与送礼物信息

- 2020.5.7
> +初步添加UI界面，采用PyQt，可显示实时弹幕和礼物信息

- 2020.5.8
> +实时人气刷新，主播粉丝按规律刷新<br>
> +连接建立与断开逻辑优化，防止多次创建wss<br>
> +添加连接建立与断开时弹幕鸡内的提示信息<br>
> +添加.gitignore<br>
> -房间id输入控件变为QLineEdit

## 参考资料：
- [websocket-client](https://github.com/websocket-client/websocket-client)
- [B站直播弹幕ws协议分析](https://daidr.me/archives/code-526.html)
- 代码灵感来自 [copyliu/bililive_dm](https://github.com/copyliu/bililive_dm)

---

> 特别感谢 [老e](https://live.bilibili.com/5050) 提供的海量弹幕测试（（（（（（
