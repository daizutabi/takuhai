import click
from takuhai.convert import convert


@click.group()
def cli():
    pass


@cli.command(name='convert')
@click.argument('path')
@click.option('--root', '-r', default='.')
def convert_command(path, root):
    convert(path, root)


@cli.command(name='serve')
# @click.argument('path')
# @click.option('--root', '-r', default='.')
def serve_command():
    print(1)


if __name__ == '__main__':
    cli()
