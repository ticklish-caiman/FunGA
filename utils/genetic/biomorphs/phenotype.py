from PIL import Image, ImageDraw

from utils.genetic.biomorphs.population import generate_biomorph


def draw_biomorph(biomorph=None, img_size=(300, 300)):
    if biomorph is None:
        biomorph = generate_biomorph()
    img = Image.new('RGB', img_size, color='white')
    draw = ImageDraw.Draw(img)

    # draw body
    xy = (biomorph.body['x1'], biomorph.body['y1'], biomorph.body['x1'] + biomorph.body['width'],
          biomorph.body['y1'] + biomorph.body['height'])
    draw.ellipse(xy, fill=biomorph.body['color'])

    # draw head
    xy = (biomorph.head['x1'], biomorph.head['y1'], biomorph.head['x1'] + biomorph.head['width'],
          biomorph.head['y1'] + biomorph.head['height'])
    draw.ellipse(xy, fill=biomorph.head['color'])

    for part in biomorph.legs:
        # adding legs
        if part['type'] == 'line':
            draw.line((part['x1'], part['y1'], part['x2'], part['y2']),
                      fill=part['color'], width=part['width'])
        # add foot
        if part['type'] == 'ellipse':
            xy = (part['x1'], part['y1'], part['x1'] + part['width'],
                  part['y1'] + part['height'])
            draw.ellipse(xy, fill=part['color'])



    return img