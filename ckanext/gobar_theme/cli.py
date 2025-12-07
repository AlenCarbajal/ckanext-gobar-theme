import click


@click.group(short_help="gobar_theme CLI.")
def gobar_theme():
    """gobar_theme CLI.
    """
    pass


@gobar_theme.command()
@click.argument("name", default="gobar_theme")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [gobar_theme]
