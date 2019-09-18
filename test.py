#!/usr/bin/env python
import click

@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--name', default='', help='Who are you?')
@click.argument('filename', default='foo')
def cli(verbose,name, filename):
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo("Hello World")
    click.echo('Bye {0}'.format(name))
    click.echo(f"filename: {filename}")

cli()