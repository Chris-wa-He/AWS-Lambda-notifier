import boto3
import json

from botocore.client import logger
from botocore.exceptions import ClientError


class claudeHelper:

    def __init__(self, region="us-east-1", model_id="anthropic.claude-3-haiku-20240307-v1:0",
                 anthropic_version="bedrock-2023-05-31", max_tokens=1024, system_prompt="", enable_debug=False):

        self.enable_debug = enable_debug

        self.region = region
        self.model_id = model_id
        self.anthropic_version = anthropic_version
        self.max_tokens = max_tokens

        self.defaultSystemPrompt = """
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

        # Set the system prompt. Use systemPrompt if it is provided and not a empty string, otherwise use the default system prompt
        self.systemPrompt = system_prompt or self.defaultSystemPrompt

        if self.enable_debug:
            print("---Debug info---")
            print("LLM region:" + self.region)
            print("Model ID:" + self.model_id)
            print("Anthropic version:" + self.anthropic_version)
            print("Max tokens:" + str(self.max_tokens))
            print("System prompt:" + self.systemPrompt)
            print("Enable debug:" + str(self.enable_debug))
            print("---End of Debug info---")

    def invoke_claude_3_with_text(self, prompt):
        """
        Invokes Anthropic Claude 3 Sonnet to run an inference using the input
        provided in the request body.

        :param prompt: The prompt that you want Claude 3 to complete.
        :return: Inference response from the model.
        """

        # Initialize the Amazon Bedrock runtime client
        client = boto3.client(
            service_name="bedrock-runtime", region_name=self.region
        )

        # Invoke Claude 3 with the text prompt
        model_id = self.model_id

        try:
            response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(
                    {
                        "anthropic_version": self.anthropic_version,
                        "max_tokens": self.max_tokens,
                        "messages": [
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": self.systemPrompt % prompt}],
                            }
                        ],
                    }
                ),
            )

            # Process and print the response
            result = json.loads(response.get("body").read())
            input_tokens = result["usage"]["input_tokens"]
            output_tokens = result["usage"]["output_tokens"]
            output_list = result.get("content", [])

            print("Invocation details:")
            print(f"- The input length is {input_tokens} tokens.")
            print(f"- The output length is {output_tokens} tokens.")

            if self.enable_debug:
                print("---Debug info---")
                print(f"- The model returned {len(output_list)} response(s):")
                for output in output_list:
                    print(output)
                print("---End of Debug info---")

            # return result
            return output_list[0]["text"]

        except ClientError as err:
            logger.error(
                "Couldn't invoke Claude 3. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
