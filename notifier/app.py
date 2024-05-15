import boto3
import os

from botocore.exceptions import ClientError

from telegram import Telegram
from alarm import Alarm
from claude import claudeHelper

send_msg_url = os.environ['SEND_MSG_URL']

bot_token_secret_arn = os.environ['BotTokenSecret_ARN']
chat_id_secret_arn = os.environ['ChatIdSecret_ARN']

enableDebug = os.environ['ENABLE_DEBUG']
enableLlm = os.environ['EnableLLM']
llmRegion = os.environ['LLM_REGION']
llmModelID = os.environ['LLM_MODEL_ID']
anthropicVersion = os.environ['Anthropic_Version']
llmMaxTokens = os.environ['LLM_Max_Tokens']
systemPrompt = os.environ['System_Prompt']

secret_manager_client = boto3.client('secretsmanager')

# Get bot token from Secrets Manager
bot_token_secret_response = secret_manager_client.get_secret_value(
    SecretId=bot_token_secret_arn
)
bot_token = bot_token_secret_response['SecretString']

# Get chat ID from Secrets Manager
chat_id_secret_response = secret_manager_client.get_secret_value(
    SecretId=chat_id_secret_arn
)
chat_id = chat_id_secret_response['SecretString']

# Combine send message api url with bot token
send_msg_api_url = send_msg_url.format(bot_token)

# Initial Telegram handler
telegram = Telegram(send_msg_api_url)


def lambda_handler(event, context):
    print(event)
    msg = msg_format(event)
    print("Original message:" + msg)

    if enableLlm == "true":
        claude = claudeHelper(region=llmRegion, model_id=llmModelID,
                              anthropic_version=anthropicVersion, max_tokens=int(llmMaxTokens),
                              system_prompt=systemPrompt,
                              enable_debug=bool(enableDebug))

        try:
            llmRsp = claude.invoke_claude_3_with_text(prompt=msg)
            msg = llmRsp + "\n\n------------------\nOriginal message:\n" + msg
        except ClientError as err:
            print("Invoke Claude 3 error:")
            print(err.response["Error"]["Code"])
            print(err.response["Error"]["Message"])

    tg_alarm = Alarm(

        description=msg,
    )

    telegram.send_text_msg(chat_id, tg_alarm)

    response = {
        "statusCode": 200,
        "body": "Message Sent."
    }

    return response


def msg_format(event):
    try:
        # 消息来源是SNS，取 $.Records[0].Sns.Message，并对字符串进行一些处理，确保发送时可以正常显示
        msg = event['Records'][0]['Sns']['Message']

        # 进行字符串处理后返回，以确保IM客户端正确显示
        msg = msg.replace("\\n", "\n")
        if msg[0] == '\"' and msg[-1] == '\"':
            msg = msg[1:-1]

        return msg
    except:
        # 消息来源不是SNS，直接返回
        return event
