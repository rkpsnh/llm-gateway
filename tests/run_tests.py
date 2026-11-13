import requests,json
import pytest
from hello_llm import ask, LLMUnavailableError, LLMTimeOutError, LLMUpstreamError, MODEL

class TestGateway:
    pass

if __name__=="__main__":
    # Define URL
    URL = "http://localhost:8000/chat"

    # Define payload
    payload = {
        "prompt":""
    }

    # Requests.post to URL
    # If status code is ok, then r.json[response]
    def loadTestCases():
        with open("tests.json") as f:
            tests = json.load(f)
            for test in tests:
                r = requests.post(URL, json=payload, timeout=60)
                response = r.json()["reply"]
                print(response)
    loadTestCases()

# Error at   File "/home/ravikant/Documents/ai_engineering/llm-gateway/tests/run_tests.py", line 3, in <module>
#     from hello_llm import ask, LLMUnavailableError, LLMTimeOutError, LLMUpstreamError, MODEL
# ModuleNotFoundError: No module named 'hello_llm'