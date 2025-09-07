import requests
import click

def getPhi(user_input, model='phi3:mini'):
    # This connects to your LOCAL Ollama server
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": user_input,
        "stream": False
    }

    response = requests.post(url, json=data)
    return response.json()['response']

@click.command()
@click.option('--user_input', prompt='Enter your message here')
def main(user_input):
    response = getPhi(user_input)
    click.echo(f"Agent: {response}")

if __name__ == "__main__":
    main()
