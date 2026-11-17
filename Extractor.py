import json
import requests
from models import DeveloperProfile


import json 
import requests

LLAMA_CPP_URL = "http://localhost:8080/v1/chat/completions"

def extractor_developer_profile(chat_history: list[dict]) -> DeveloperProfile: 

    json_schema = DeveloperProfile.model_json_schema()

    system_prompt = (
        "You are a precise data extraction engine. Analyze the conversation history "
        "and extract the user's professional profile matching the exact JSON schema provided. "
        "Extract only what was explicitly stated in the conversation."
    )
    messages = [{
        "role": "system", 
        "content": system_prompt
    }] + chat_history
    messages.append({
      "role": "user",
        "content": "Please output the final extracted profile JSON based on our conversation."
    })

    payload = {
        "model": "local-model",
        "messages": messages,
        "temperature": 0,
        "response_format":{
            "type": "json_schema",
            "json_schema":{
                "name": "developer_profile_schema",
                "strict": True,
                "schema": json_schema,
            }
        }
    }

    try:
        response = requests.post(LLAMA_CPP_URL, json=payload, timeout=60)
        response.raise_for_status()

        result_content = response.json()["choices"][0]["message"]["content"]

        data_dict = json.loads(result_content)

        profile_object = DeveloperProfile.model_validate(data_dict)

        return profile_object
        
    except requests.exceptions.ConnectionError:
        print("\n[ERROR]: Could not connect to local llama.cpp server. Is it running on port 8080?")
        raise
    except Exception as e:
        print(f"\n[EXTRACTION ERROR]: {e}")
        raise
        
        
    
