import pandas as pd
from PIL import Image
import numpy as np
import os
from tqdm import tqdm

csv_filename = 'output.csv'
df=pd.read_csv(csv_filename)

def convert_to_greyscale(input_path, output_path,index):
    global df,csv_filename

    img = Image.open(input_path)
    img = img.resize((127,96))
    width, height = img.size
    greyscale_img = Image.new('L', (width, height))
    img_pixels = img.load()
    greyscale_pixels = greyscale_img.load()  
    for x in range(width):
        for y in range(height):
            red, green, blue = img_pixels[x, y]
            grey_value = int(0.299 * red + 0.587 * green + 0.114 * blue)
            greyscale_pixels[x, y] = grey_value
    greyscale_img.save(output_path)
    x_array = np.array(img).flatten()
    y_array = np.array(greyscale_img).flatten()
    
    data=np.append(x_array,y_array)
    
    if os.path.exists(csv_filename):
        df[str(index)] = data
    else:
        df = pd.DataFrame(data, columns=[str(index)])
    


if __name__ == "__main__":
    input_folder = './imagedata/train'
    output_folder = './output_greyscale'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_list = [filename for filename in os.listdir(input_folder) if filename.endswith((".bmp", ".jpg"))]
    index=0
    for filename in tqdm(file_list, desc="Converting to greyscale", unit="image"):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, f"{filename[:-4]}_greyscale.bmp")
        if index<2000:
            convert_to_greyscale(input_file, output_file,index)
            index +=1
    df.to_csv(csv_filename, index=False)
