from openai import OpenAI
from prompts.main_prompt import MAIN_SYSTEM_PROMPT
import json
from dotenv import load_dotenv
from judge import judgeMe

load_dotenv()

client = OpenAI()


def main():
    query = input("What would you like me to solve?\n")

    messages = [{
        "role": "system",
        "content": MAIN_SYSTEM_PROMPT
    }, {
        "role": "user",
        "content": query
    }]

    while (True):
        response = client.chat.completions.create(
            model="gpt-5.2",
            messages=messages
        )

        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content})

        parsedContent = json.loads(response.choices[0].message.content)

        if (parsedContent["step"] == "START"):
            print(parsedContent["content"])
            continue

        elif (parsedContent["step"] == "THINK"):

            print(parsedContent["content"])
            judged = judgeMe(messages)

            parsedJudge = json.loads(judged)

            if (parsedJudge["correct"] == "true"):

                print("✅ Approved by claude: ", parsedContent["content"])
                messages.append({"role": "assistant", "content": judged})

            elif (parsedContent["correct"] == "false"):

                print("❌ Denied by claude: ", parsedContent["content"])
                messages.append(
                    {"role": "assistant", "content": json.dumps({"step": "END", "content": "Terminating..."})})
            continue

        elif (parsedContent["step"] == "END"):
            print(parsedContent["content"])
            break


main()
