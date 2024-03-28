import base64
from io import BytesIO

from PIL import Image, ImageDraw

from utils.genetic.biomorphs.population import Biomorph


def draw_biomorph(biomorph=None, img_size=(500, 500)):
    if biomorph is None:
        bm = Biomorph()
        biomorph = bm.generate_biomorph()
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

    # Draw eyes
    draw.ellipse((biomorph.left_eye['x1'] - biomorph.left_eye['radius'],
                  biomorph.left_eye['y1'] - biomorph.left_eye['radius'],
                  biomorph.left_eye['x1'] + biomorph.left_eye['radius'],
                  biomorph.left_eye['y1'] + biomorph.left_eye['radius']),
                 fill=biomorph.left_eye['color'])
    draw.ellipse((biomorph.right_eye['x1'] - biomorph.right_eye['radius'],
                  biomorph.right_eye['y1'] - biomorph.right_eye['radius'],
                  biomorph.right_eye['x1'] + biomorph.right_eye['radius'],
                  biomorph.right_eye['y1'] + biomorph.right_eye['radius']),
                 fill=biomorph.right_eye['color'])

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


def get_base64_of_image(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    base64_encoded_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{base64_encoded_img}"
