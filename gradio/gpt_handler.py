import os
import json
from dotenv import load_dotenv

# Add OpenAI import
from openai import AzureOpenAI

from prompt_templates import get_system_prompt

# OpenAI API 키를 .env에서 불러옵니다.
load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.getenv("AZURE_SEARCH_KEY")
azure_search_index = os.getenv("AZURE_SEARCH_INDEX")

def call_gpt(prompt: str) -> str:
    try:
        client = AzureOpenAI(
            base_url=f"{azure_oai_endpoint}/openai/deployments/{azure_oai_deployment}/extensions",
            api_key=azure_oai_key,
            api_version="2023-09-01-preview")

        extension_config = dict(dataSources = [
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": azure_search_endpoint,
                    "key": azure_search_key,
                    "indexName": azure_search_index
                }
            }
        ])

        response = client.chat.completions.create(
            model = azure_oai_deployment,
            messages = [
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            max_tokens = 1000,
            temperature = 0.5,
            extra_body = extension_config
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] GPT 호출 실패: {e}"
