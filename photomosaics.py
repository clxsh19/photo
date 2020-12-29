from PIL import Image
import os
import math
import json

Filename = 'pokemon.jpg' #input("Filename: ")
path = os.path.abspath(Filename)
IMAGE = Image.open(path)

WIDTH, HEIGHT = IMAGE.size
SIDE = 10
NEW_IMAGE = Image.new(mode = "RGB", size = (WIDTH ,HEIGHT), color = None)
DIV = SIDE*SIDE

def create_file():
    File = open("cache.json", "w")
    print("Creating json file...")
    Folder_name = input("Source_Folder name: ")
    folder_path = os.path.abspath(Folder_name)
    
    data = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        source_image = Image.open(file_path)
        resize_image =  source_image.resize((10, 10))

        pixels = resize_image.getdata()
        r2, g2, b2 = Add_all_pixels(pixels)
        r2, g2, b2 = r2//DIV, g2//DIV, b2//DIV

        # adding rgb value to dict
        data.update({filename : (r2,g2,b2)})

    json.dump(data, File)  
    File.close()

def pixelate(image, i, j, r, g, b):
    px_image = image.load()
    n = HEIGHT - SIDE
    if i <= n:
        for i_index in range(i ,i + SIDE):
            for j_index in range(j ,j + SIDE):
                px_image[j_index, i_index] = (r, g, b)

def Add_all_pixels(pixels):
    r, g, b = 0, 0, 0
    for i in range(len(pixels)):
        r += pixels[i][0]
        g += pixels[i][1]
        b += pixels[i][2]
    return r, g, b

def Calculate_Similarity(r1, g1, b1, r2, g2, b2):
    similarity = math.sqrt( ((r2 - r1)**2) + ((g2 - g1)**2) + ((b2 - b1)**2) )
    return (round(similarity))

def source_image(i, j, new_img, r1, g1, b1):
    # if cache file exists open it
    Filename_ = 'cache.json'
    path_ = os.path.abspath(Filename_)
    RGB_VALS = open(path_ ,"r")
    Data = json.load(RGB_VALS)
    Value = 300

    # enter folder name of source images
    folder_name = 'data'
    folder_path = os.path.abspath(folder_name)
    for filename in os.listdir(folder_path):
        r2, g2, b2 = Data[filename][0], Data[filename][1], Data[filename][2]  
        sim_value = Calculate_Similarity(r1 ,g1 ,b1 ,r2 ,g2 ,b2)
        if sim_value <= Value:
            Value = sim_value
            sim_filename = filename

    file_path = os.path.join(folder_path, sim_filename)
    source_img = Image.open(file_path)
    resize_img =  source_img.resize((SIDE, SIDE))
    Image.Image.paste(new_img, resize_img, (j,i))

def run(image, NEW_IMAGE):
    # cropping a part of main_image
    for i in range(0 ,HEIGHT ,SIDE):
        for j in range(0 ,WIDTH ,SIDE):
            # dimensions for cropping
            dimensions = (j ,i ,j + SIDE ,i + SIDE)
            Crop_image = image.crop(dimensions)   
            
            # getting cropped image pixels
            Crop_img_pixels = Crop_image.getdata()
            r1, g1, b1 = Add_all_pixels(Crop_img_pixels)
            # average rgb of cropped image
            r1, g1, b1 = r1//DIV, g1//DIV, b1//DIV
            source_image(i, j, NEW_IMAGE, r1, g1, b1)
try:
    check = open("cache.json")
    check.close()
except:
    create_file()

print("running...")
run(IMAGE, NEW_IMAGE)
NEW_IMAGE.show()

# saving
name = input("Name: ")
NEW_IMAGE = NEW_IMAGE.save("%s.jpg" %(name))