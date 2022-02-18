import boto3
import os

from feishu import Feishu
from alarm import Alarm

secretTokenArn = os.environ['TOKEN_ARN']

# Get chat bot token from Secrets Manager
secret_manager_client = boto3.client('secretsmanager')
get_secret_value_response = secret_manager_client.get_secret_value(
        SecretId=secretTokenArn
    )
secretToken = get_secret_value_response['SecretString']

# Initial Feishu handler
feishu=Feishu(secretToken)

def lambda_handler(event, context):
    print(event)
    msg = msg_format(event)
    print(msg)

    fsAlarm = Alarm(

        description=msg,
    )

    feishu.send_text_msg(fsAlarm)

    response = {
        "statusCode": 200,
        "body": "Message Sent."
    }

    return response

def msg_format(event):
    try:
        #消息来源是SNS，取 $.Records[0].Sns.Message，并对字符串进行一些处理，确保发送时可以正常显示
        msg = event['Records'][0]['Sns']['Message']

        #进行字符串处理后返回，以确保IM客户端正确显示
        msg = msg.replace("\\n", "\n")
        if msg[0] == '\"' and msg[-1] == '\"' :
            msg = msg[1:-1]

        return msg
    except:
        #消息来源不是SNS，直接返回
        return event