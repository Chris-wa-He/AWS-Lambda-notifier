# Telegram-Notifier Telegram 告警通知

我们在使用AWS时偶尔会在管理员邮箱中收到AWS关于EC2维护信息的通知邮件，这些邮件很容易淹没在收件箱中，没有得到及时处理。很多客户希望能够更及时收到这类消息，比如从微信或是钉钉等即时通信软件收到这类消息通知。

微信或钉钉等即时通信工具均提供了消息接口，第三方应用获取授权后，通过调用这些接口即可往客户端发送消息。在AWS上可以在EventBridge/Cloudwatch Event中配置事件规则，即可以触发一个Lambda运行微信/钉钉接口调用的处理逻辑。讲解这方面设计的博客和技术文章也比较多了，具体可以参考附录的一些链接。

这个项目会多做一点点，提供一个无须编写代码快速部署飞书告警通知的功能。在Serverless Application Repository 中可以通过填入 Telegram 机器人接口相关的参数，即可快速部署整套 Telegram 告警通知的相关组件，涉及的 AWS 服务包括 EventBridge, SNS, Lambda 和 Secrets Manager 等。如下是整体的部署架构：

为方便演示，这个应用部署时创建了两个EventBridge的Rule，一个是捕获EC2的状态变化事件（如开关机），另一个是捕获EC2健康事件（如EC2计划维护事件）。因此部署后可以通过简单的启动或关闭EC2实例来检查是否可以在 Telegram 收到通知。

## 致谢

本项目基于 Niko Feng 企业微信对接[项目](https://github.com/nikosheng/wechat-lambda-layer-sam) 与 Randy Lin SAR部署[项目](https://github.com/linjungz/wechat-notifier.git) 的基础上修改 Telegram 对接实现及部署模板完成。在此对 Niko 与 Randy 表示感谢！
