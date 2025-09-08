import requests
import click
import subprocess


def getPhi(user_input, system_prompt="be helpful", model='phi3:mini'):
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
        click.echo("Choosing tool")
        tool = chooseTool(user_input)
        command = getCommand(tool)
        if command:
            print("command present")
            commandResults = subprocess.run(command, shell=True, capture_output=True, text=True)
            print(commandResults.stdout)

def getCommand(tool):
    print("geting command")
    lines = tool.split('\n')
    for line in lines:
        if line and line.strip().startswith("COMMAND:"):
            arg = line.replace("COMMAND:", "")
            print(f"ARG: {arg}")
            return arg

if __name__ == "__main__":
    main()

def chooseTool(user_input):
    system_prompt = """
    Your job is to choose the most relevent tool out of the following list and respond in the response format with no extra text:
       timetrack: a tool that tracks time
       timetrack tool commands:
           timetrack start: starts the timer
           timetrack stop: stops the Timer


    response format:
        TOOL: [insert tool name here]
        COMMAND: [insert relevent command here]
    """
    tool = getPhi(user_input, system_prompt)
    print(tool)
    return tool
