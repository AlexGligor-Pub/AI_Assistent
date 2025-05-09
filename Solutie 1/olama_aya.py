import requests
import json

def prompt_aya(prompt_text: str) -> str:
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "ayahtml", #"ayav4",
        "prompt": prompt_text
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, stream=True)

        if response.status_code == 200:
            result = ""
            for line in response.iter_lines():
                if line:
                    json_line = json.loads(line.decode('utf-8'))
                    if 'response' in json_line:
                        result += json_line['response']
            return result
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Exception: {e}"