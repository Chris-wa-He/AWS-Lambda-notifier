import boto3
import json

from botocore.client import logger
from botocore.exceptions import ClientError


class converseApiCaller:

    def __init__(self, region="us-east-1", model_id="amazon.nova-pro-v1:0", max_tokens=1024, prompt="",
                 enable_debug=False):
        self.enable_debug = enable_debug

        self.region = region
        self.model_id = model_id
        self.max_tokens = max_tokens

        self.defaultPrompt = """
                    You are an advanced content organizer. Your goal is to summarize and organize the input message following the format of <example>, with the input contained within <msg>. The final output should only include the content within <msg>, without any additional extrapolation or insights beyond that. First, a brief one-sentence summary of the <msg> content, placed after the header 'AWS Notification'. If there are descriptive fields in the content, please translate them into a different language. Specialized terms such as EC2, RDS, etc. need not be translated.If there is a URL in the message, please keep it as is. The header 'AWS Notification' must be retained.Output the result in text without xml tag, with the language being Chinese first, followed by English.

        <example>
        AWS 提示信息

        信息摘要：一个EC2实例被启动了。

        EC2状态变化告警: 
        时间: 2024-04-26T02:16:20Z 
        区域: us-west-2 
        实例id: i-01e00af4bfbc1b6c3 
        状态: running
        URL: https://console.aws.amazon.com/costmanagement/home#/anomaly-detection/monitors/6723d2b9-885c-475e-9cfe-1214a512ee64/anomalies/414aaa55-e5d5-4775-874e-89a6783a57e

        AWS notification

        Summary: An EC2 instance was started.

        EC2 instance status change alert:
        Time: 2024-04-26T02:16:20Z
        Region: us-west-2
        Instance ID: i-01e00af4bfbc1b6c3
        Status: running
        URL: https://console.aws.amazon.com/costmanagement/home#/anomaly-detection/monitors/6723d2b9-885c-475e-9cfe-1214a512ee64/anomalies/414aaa55-e5d5-4775-874e-89a6783a57e
        </example>

        <msg>
        %s
        </msg>
                    """

        # Set the prompt. Use prompt if it is provided and not an empty string, otherwise use the default prompt
        self.prompt = prompt or self.defaultPrompt

        if self.enable_debug:
            print("---Debug info---")
            print("LLM region:" + self.region)
            print("Model ID:" + self.model_id)
            print("Max tokens:" + str(self.max_tokens))
            print("Prompt:" + self.prompt)
            print("Enable debug:" + str(self.enable_debug))
            print("---End of Debug info---")

    def invoke_converse_api(self, input_text):
        """
        Invokes bedrock to run an inference using the input
        provided in the request body.

        :param input_text: The imput text that you want LLM to handle.
        :return: Inference response from the model.
        """

        # Initialize the Amazon Bedrock runtime client
        client = boto3.client(
            service_name="bedrock-runtime", region_name=self.region
        )

        # Invoke LLM with the text prompt
        model_id = self.model_id

        inferenceConfig = {
            "maxTokens": self.max_tokens
        }

        message = {
            "role": "user",
            "content": [
                {
                    "text": self.prompt % input_text
                }
            ]
        }

        messages = [message]

        try:
            response = client.converse(
                modelId=model_id,
                inferenceConfig=inferenceConfig,
                messages=messages
            )

            # Process and print the response
            input_tokens = response['usage']['inputTokens']
            output_tokens = response['usage']['outputTokens']
            total_tokens = response['usage']['totalTokens']
            latencyMs = response['metrics']['latencyMs']
            return_msg = response['output']['message']

            print("Invocation details:")
            print(f"- The input length is {input_tokens} tokens.")
            print(f"- The output length is {output_tokens} tokens.")
            print(f"- The Total tokens are {total_tokens}.")
            print(f"- The latency is {latencyMs} ms.")

            if self.enable_debug:
                print("---Debug info---")
                print("The model returned below message:")
                print(f"role: {return_msg['role']}")
                print(f"content: {return_msg['content']}")
                print("---End of Debug info---")

            # return result
            return response['output']['message']['content'][0]['text']

        except ClientError as err:
            logger.error(
                "Couldn't invoke LLM. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
