import click
from display_tools.font_builder import Builder, Matrix

@click.command()
@click.argument('file')
@click.argument('size')
@click.option('--base', default=7)
@click.option('--preview', is_flag=True)
@click.option('--scale', default=1)
@click.option('--font-class', default=None)
def build(file, size, base, preview, scale, font_class):
    
    builder = Builder(file, int(size), base)
    
    if preview:
        from PIL import Image, ImageColor

        display = Matrix()
        text = builder.render('abcdefghijklmnopqrstuvwxyz\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n1234567890\n?!<>{}[],.=+-_')
        display = display.over(text, x=10, y=10).scale(scale)
        im = Image.new('RGB', (display.width + 10*scale, display.height + 10*scale))
        white = ImageColor.getcolor('white', 'RGB')
        black = ImageColor.getcolor('black', 'RGB')
        im.paste(white, [0, 0, im.size[0], im.size[1]])
        for x, y, _ in display:
            im.putpixel((x, y), black)
        im.show()
    else:

        if font_class is not None:
            click.echo(f'class {font_class}(Font):')
            click.echo('    def __init__(self):')
            click.echo(f'        super().__init__({builder})')
        else:
            click.echo(builder)

if __name__ == '__main__':
    build()