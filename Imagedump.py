import os
from app import db,Images,app
import base64


def add_image(Id,Image1path,Image2path):
    with open(Image1path, 'rb') as f:
        image1_binary = f.read()
    
    with open(Image2path, 'rb') as f:
        image2_binary = f.read()
    
    # Encode binary data as base64 string
    image1_data = base64.b64encode(image1_binary).decode('utf-8')
    image2_data = base64.b64encode(image2_binary).decode('utf-8')
    new_image = Images(id = Id ,first_image = image1_data,second_image = image2_data)
    with app.app_context():
        db.session.add(new_image)
        db.session.commit()
    return 'Images added to database'

# Define paths to image folders
folder1 = r'C:\Users\Ch Abdullah\Downloads\Compressed\Handwriting data\ImageGrad'
folder2 = r'C:\Users\Ch Abdullah\Downloads\Compressed\Handwriting data\ImageSolid'
count =0
# Loop through files in folder1 and check for matching filename in folder2
for filename1 in os.listdir(folder1):
    if filename1[-1] == '~':  # skip temporary files created by some text editors
        continue
    for filename2 in os.listdir(folder2):
        if filename2[-1] == '~':
            continue
        if filename1[:-1] == filename2[:-1]:  # check for matching filenames except for last character
            file1_id = filename1.split("_")[0]
            file2_id = filename2.split("_")[0]
            print(file2_id)
            print(file1_id)
            add_image(file1_id,folder1+"\\"+filename1,folder2+"\\"+filename2)
            count +=1
            # Open and read in images using Pillow
            #with Image.open(folder1 + filename1) as img1:
                #with Image.open(folder2 + filename2) as img2:
                    # Add images to database using SQLAlchemy
                    #add_image(filename1[:-1], img1.tobytes() + img2.tobytes())
print(count)