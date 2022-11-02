# WeChat-Notifier 微信告警通知

我们在使用AWS时偶尔会在管理员邮箱中收到AWS关于EC2维护信息的通知邮件，这些邮件很容易淹没在收件箱中，没有得到及时处理。很多客户希望能够更及时收到这类消息，比如从微信或是钉钉等即时通信软件收到这类消息通知。

微信或钉钉等即时通信工具均提供了消息接口，第三方应用获取授权后，通过调用这些接口即可往客户端发送消息。在AWS上可以在EventBridge/Cloudwatch Event中配置事件规则，即可以触发一个Lambda运行微信/钉钉接口调用的处理逻辑。讲解这方面设计的博客和技术文章也比较多了，具体可以参考附录的一些链接。

这个项目会多做一点点，提供一个无须编写代码快速部署微信告警通知的功能。在Serverless Application Repository 中可以通过填入三个跟微信接口相关的参数，即可快速部署整套微信告警通知的相关组件，涉及的 AWS 服务包括 EventBridge, SNS, Lambda 和 Secrets Manager 等。如下是整体的部署架构：

![整体部署架构](images/architecture.png)

为方便演示，这个应用部署时创建了两个EventBridge的Rule，一个是捕获EC2的状态变化事件（如开关机），另一个是捕获EC2健康事件（如EC2计划维护事件）。因此部署后可以通过简单的启动或关闭EC2实例来检查是否可以在微信端收到通知。

## 在 Serverless Application Repository 中部署此应用

可以在 SAR 中搜索 `wechat-notifier` 查到本应用（注意因为本项目会创建 EventBridge 到 SNS Publish 权限，所以按下图进行勾选。

![查找](images/search_sar.png)

## 致谢

本项目使用的企业微信对接代码是在 Niko Feng 之前[项目](https://github.com/nikosheng/wechat-lambda-layer-sam)的基础上增加了异常处理和将密钥保存在Secrets Manager等调整。在此对 Niko 表示感谢！

## 更新历史

2021-03-25:
调整 SNS Access Policy，权限由原来只能由 SNS 所在帐号 EventBridge 发布消息，改为由 SNS 所在帐号所有 AWS 服务均可发布消息，方便用户从其他 AWS 服务如 RDS 等设置事件通知告警并通知微信

2022-10-16:
添加 AWS Cost Anomaly Detection 集成。

2022-11-2:
添加 Amazon GuardDuty 集成。

## 附录

[AWS博客：基于AWS Serverless 一键启用微信/钉钉告警通知
](https://aws.amazon.com/cn/blogs/china/enable-wechat-dingtalk-alarm-notification-with-one-click-based-on-aws-serverless/)

[AWS博客：企业微信、钉钉接收 Amazon CloudWatch 告警
](https://aws.amazon.com/cn/blogs/china/enterprise-wechat-and-dingtalk-receiving-amazon-cloudwatch-alarms/)