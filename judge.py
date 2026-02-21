import anthropic
from prompts.judge_prompt import generateJudgePrompt
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


def judgeMe(history: list[dict[str, str]]):
    if (history.__len__ == 2):
        return

    userMessage = history[1]
    assistantMessages = history[2:history.__len__()]

    allMessages = [userMessage, *assistantMessages]

    systemPromptWithHistory = generateJudgePrompt(json.dumps(allMessages))

    message = client.messages.create(
        model="claude-opus-4-1-20250805",
        max_tokens=1000,
        system=systemPromptWithHistory,
        messages=[
            {
                "role": "user",
                "content": "Is the last THINK step valid? Go through the message history recieved from the first LLM and reply with the specified JSON format.",
            }
        ],
    )

    return message.content[0].text if message.content[0].type == "text" else ""
