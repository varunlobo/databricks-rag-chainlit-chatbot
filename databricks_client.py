import os
import token
import requests
from dotenv import load_dotenv

load_dotenv()


def call_databricks_rag(user_question: str) -> str:
    url = os.getenv("DATABRICKS_ENDPOINT_URL")
    token = os.getenv("DATABRICKS_TOKEN")

    

    if not url or not token:
        return "Missing Databricks endpoint URL or token. Check your .env file."

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
    "dataframe_records": [
        {
            "message": user_question
        }
    ]
}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Databricks endpoint error {response.status_code}: {response.text}"

    data = response.json()

    try:
        return data["output"][0]["content"][0]["text"]
    except Exception:
        return str(data)
    

if __name__ == "__main__":
    question = "Hello"

    answer = call_databricks_rag(question)

    print("\nResponse from Databricks:\n")
    print(answer)