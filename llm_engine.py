import requests
import json

class LLM:
    def __init__(
        self,
        api_key,
        model="xiaomi/mimo-v2-flash:free",
        base_url="https://openrouter.ai/api/v1/chat/completions"
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    def reason(self, prompt, max_tokens):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "AI Project Analyzer"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3
        }

        try:
            r = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=120
            )

            # ---------- HARD FAIL ----------
            if r.status_code != 200:
                return (
                    f"LLM ERROR ({r.status_code})\n\n"
                    f"{r.text}"
                )

            data = r.json()

            # ---------- VALID RESPONSE ----------
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]

            # ---------- API RETURNED ERROR ----------
            if "error" in data:
                return (
                    "LLM ERROR RESPONSE\n\n"
                    f"{json.dumps(data['error'], indent=2)}"
                )

            # ---------- UNKNOWN FORMAT ----------
            return (
                "LLM UNKNOWN RESPONSE FORMAT\n\n"
                f"{json.dumps(data, indent=2)}"
            )

        except requests.exceptions.Timeout:
            return "LLM ERROR: Request timed out"

        except requests.exceptions.RequestException as e:
            return f"LLM REQUEST ERROR: {str(e)}"

        except Exception as e:
            return f"LLM INTERNAL ERROR: {str(e)}"
