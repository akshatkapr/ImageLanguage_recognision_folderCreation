import pytesseract
from PIL import Image
from pytesseract import Output
from functools import reduce
import os
import glob
import shutil

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-ocr\\tesseract.exe"
check_lang = ["ces","fra","tha","ukr","rus","pol","chi_sim","chi_tra","eng","dan","fil","deu","ell","ind","ita","jpn","kor","nor","ron","spa","swe","tur","vie","fin","msa"]
c = 0
def Average(result_list):
    return reduce(lambda a, b: a + b, result_list) / len(result_list)

def SpaceValueremoval(imageconf):
    result_list = []
    [result_list.append(x) for x in imageconf if x != -1]
    return Average(result_list)

    
#creating folders
for a in check_lang :
    os.mkdir(a)
print("folders Created ")

for img in glob.glob('C:\Test\*.png'):
    c = c + 1
    src_dir = os.path.abspath(img)
    print("source Directory " , src_dir)
    parent_dir = os.path.dirname(src_dir)
    print("parent Directory " , parent_dir)
    #default values to compare with other languages

    result = pytesseract.image_to_data(Image.open(src_dir),lang="eng",output_type=Output.DICT)
    #extracting conf colomn
    imageconf = result["conf"]
    #removing -1 value which is given to space in sentence
    
    High_average_conf = SpaceValueremoval(imageconf)
    
    #compairing the conf with each language to detect
    for x in check_lang:
        result = pytesseract.image_to_data(Image.open(src_dir),lang=x,output_type=Output.DICT)
        imageconf = result["conf"]
        lang_average_conf = SpaceValueremoval(imageconf)
        if lang_average_conf > High_average_conf:
            High_average_conf = lang_average_conf
            Detected_lang = x
    
    
    dst_dir = os.path.join(parent_dir, Detected_lang)

    #rename the file
    a = parent_dir + "\\" + Detected_lang + str(c)+ ".png"
    os.rename(src_dir, a)
    print("new name " , a)

    #send the image to destination folder
    for pngfile in glob.iglob(a):
        print("pngfile " , pngfile)
        print("destination Directory copied to" , dst_dir)
        shutil.copy(pngfile, dst_dir)
    
    print("language= ",Detected_lang,"conf= ",High_average_conf)
