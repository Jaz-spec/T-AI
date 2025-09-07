import click

@click.command()
def hello():
    """prints a message"""
    click.echo('Hello :)')

if __name__ == '__main__':
    hello()
