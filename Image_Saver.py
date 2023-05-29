from models import db,Images
import base64

def add_image(Image):
    with open(Image, 'rb') as f:
        image_binary = f.read()

    # Encode binary data as base64 string
    image_data = base64.b64encode(image_binary).decode('utf-8')
    new_image = Images(first_image = image_data,second_image = image_data)
    images = Images.query.all()
    print(images)
    db.session.add(new_image)
    db.session.commit()
    return 'Images added to database'


