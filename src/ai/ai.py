import requests
import click
import subprocess


def getPhi(user_input, system_prompt="be helpful", model='dolphin3:latest'):
    print("CALLING AI")
    # Connects to local Ollama server
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": user_input,
        "system": system_prompt,
        "stream": False
    }

    response = requests.post(url, json=data)
    return response.json()['response']

@click.command()
@click.option('--user_input', prompt='Enter your message here')
def main(user_input):
    if user_input and user_input.split(' ', 1)[0].lower() == "timetrack":
        results = subprocess.run(user_input,
            shell=True,
            capture_output=True,
            text=True)
        print(results.stdout)
    else:
        tool = chooseTool(user_input)
        command = getCommand(user_input, tool)
        if command:
            print("MAKING TERMINAL CALL")
            commandResults = subprocess.run(command, shell=True, capture_output=True, text=True)
            print(commandResults.stdout)


if __name__ == "__main__":
    main()

def chooseTool(user_input):
    print("CHOOSING TOOL")
    system_prompt = """
    Your job is to choose the most relevent tool out of the following list and respond in the response format with no extra text:
       timetrack: a tool that tracks time
       lazygit: a tool that allows you to make commits to github

    response format:
        TOOL: [insert tool name here]
    """
    response = getPhi(user_input, system_prompt)
    tool = response.replace("TOOL:", "").strip().lower()
    if tool == "timetrack":
        return tool
    else:
        print("Error: no tool match @ tool choice")
        print(f"timetrack -> {tool}")
        return None

def getCommand(user_input, tool):
    if tool and tool == "timetrack":
        system_prompt = """
        Your job is to choose the most appropriate command to forfill the users request. Your options are:
            timetrack start: starts the timer
            timetrack stop: stops the Timer
            timetrack status: shows how long and active timer has been running for

        response format:
            COMMAND: [insert command here]
        """
        response = getPhi(user_input, system_prompt)
        command = response.replace("COMMAND:", "")
        if command in ('timetrack start', 'timetrack stop', 'timetrack status'):
            return command
        else:
            print("Error: valid command not returned")
            return None
    else:
        print("Error: no tool match @ command choice")
