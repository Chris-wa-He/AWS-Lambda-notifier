# Slack-Notifier: Slack Notification for AWS Events

We occasionally receive notification emails from AWS regarding EC2 maintenance information in our admin mailbox when using AWS. However, these emails can easily get buried in the inbox and may not be addressed promptly. Many customers wish to receive such messages more promptly, such as through instant messaging apps like Slack.

Instant messaging tools like Slack provide message interfaces, and third-party applications can send messages to clients by calling these interfaces after obtaining authorization. On AWS, you can configure event rules in EventBridge/CloudWatch Events to trigger a Lambda function to run the logic for calling the Slack Incoming Webhook interface.

This project goes a step further and provides a feature to quickly deploy Slack alert notifications without writing any code. In the Serverless Application Repository, you can fill in the parameters related to the Slack Incoming Webhook interface and quickly deploy a suite of components for Slack alert notifications. The AWS services involved include EventBridge, SNS, Lambda, and Secrets Manager. The overall deployment architecture is shown below:

![Overall Deployment Architecture](images/architecture.png)

For demonstration purposes, this application creates two EventBridge Rules during deployment: one captures EC2 state change events (such as start/stop), and the other captures AWS health events (such as EC2 scheduled maintenance events). Therefore, after deployment, you can check if you receive notifications on Slack by simply starting or stopping an EC2 instance.

## Creating a Slack Incoming Webhook and Obtaining the Webhook URL

To configure a Slack Incoming Webhook, please refer to the [official guide](https://slack.com/help/articles/115005265063-Incoming-WebHooks-for-Slack).

Obtain the Webhook URL for the Incoming Webhook, which will be used as a deployment parameter. [API documentation](https://api.slack.com/messaging/webhooks)
![Get Webhook](images/webhook.png)

## Deploying this Application in the Serverless Application Repository

You can search for `Slack-Notifier` in SAR to find this application. (Note that since this project will create EventBridge to SNS Publish permissions, you need to check the box as shown in the image below.)

![Search](images/search_sar.png)

When deploying the application, enter the entire Webhook URL for the custom bot.

![Deployment](images/deployment.png)

LLM-related deployment options:
![llm_parameter](images/llm_parameter.png)

The LLM parameters are optional, and the default values are shown in the image above. For customizing the System Prompt, please refer to [defaultSystemPrompt](layer/python/claude.py).

## Notification Effect

The notification effect is as follows:

![Notification Effect](images/notification.png)

## Message Sorting Effect with LLM

Original message:

![Original Message](images/origin_msg.png)

Sorted message:
![Sorted Message](images/sort_msg.png)

## Default Included Notification Events
* AWS Health Event
* AWS Health Abuse Event
* EC2 Instance State-change
* CloudWatch Alarm State Change

## Acknowledgments

This project is based on Niko Feng's WeChat Work integration [project](https://github.com/nikosheng/wechat-lambda-layer-sam) and Randy Lin's SAR deployment [project](https://github.com/linjungz/wechat-notifier.git), with modifications for Slack integration and deployment template implementation. We would like to express our gratitude to Niko and Randy!

## Update History

2022-02-19:
Implemented plain text alert push functionality for Slack Incoming Webhook.

2022-10-16:
Added AWS Cost Anomaly Detection integration.

2022-11-2:
Added Amazon GuardDuty integration.

2023-02-28:
1. Converted AWS service integration to a plugin-based approach. Please refer to the [project: AWS-Lambda-notifier-plugin](https://github.com/Chris-wa-He/AWS-Lambda-notifier-plugin) for more information.
2. Added Cloud Watch alarm state change as a default rule.
3. Removed AWS Cost Anomaly Detection & Amazon GuardDuty integration, which has been moved to the [project: AWS-Lambda-notifier-plugin](https://github.com/Chris-wa-He/AWS-Lambda-notifier-plugin).

2023-06-2:
Added Event Bridge name and SNS ARN as outputs for easier integration as plugin parameters.

2023-06-14:
Added capturing AWS Health Abuse Event as a default event.

2024-05-16:
Added the ability to connect to the Bedrock-managed LLM for information sorting.

2024-12-11:
Use the Converse API to call Bedrock models. The default usage model is tuned to Amazon Nova Lite.

## Appendix

[AWS Blog: Enable WeChat/DingTalk Alarm Notification with One-Click Based on AWS Serverless](https://aws.amazon.com/cn/blogs/china/enable-wechat-dingtalk-alarm-notification-with-one-click-based-on-aws-serverless/)

[AWS Blog: Enterprise WeChat and DingTalk Receiving Amazon CloudWatch Alarms](https://aws.amazon.com/cn/blogs/china/enterprise-wechat-and-dingtalk-receiving-amazon-cloudwatch-alarms/)