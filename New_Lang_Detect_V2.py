import pytesseract
from PIL import Image
from pytesseract import Output
from functools import reduce
import os
import glob
import shutil
import time
import cv2
import langid
import pycountry

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-ocr\\tesseract.exe"
check_lang = ["ces","fra","ron","ukr","rus","pol","chi_sim","chi_tra","nld","por","eng","dan","fil","deu","ell","ind","ita","jpn","kor","nor","spa","swe","tur","vie","fin","msa","tha"]
c = 0
def Average(result_list):
    return reduce(lambda a, b: a + b, result_list) / len(result_list)

def SpaceValueremoval(imageconf):
    result_list = []
    [result_list.append(x) for x in imageconf if x != -1]
    return Average(result_list)

def CompareLang(High_average_conf2, filename2):
    for x in check_lang:
        result = pytesseract.image_to_data(Image.open(filename2),lang=x,config='--psm 3',output_type=Output.DICT)
        imageconf = result["conf"]
        lang_average_conf = SpaceValueremoval(imageconf)
        if lang_average_conf > High_average_conf2:
            High_average_conf2 = lang_average_conf
            Detected_lang2 = x
    return High_average_conf2, Detected_lang2;

def imageprocessing(img2):
    images=cv2.imread(img2)
    gray=cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
    gray=cv2.threshold(gray, 0,255,cv2.THRESH_BINARY+ cv2.THRESH_OTSU)[1]
    filename2 = "{}.jpg".format(os.getpid())
    cv2.imwrite(filename2, gray)
    return filename2


Input_path = input('Enter the file path: ')

for img in glob.glob(Input_path + '\*.png'):
    t1_start = time.perf_counter()
    c = c + 1
    src_dir = os.path.abspath(img)
    print("source Directory " , src_dir)
    parent_dir = os.path.dirname(src_dir)
    #print("parent Directory " , parent_dir)

    filename = imageprocessing(img)
    
    #default values to compare with other languages

    result = pytesseract.image_to_data(Image.open(filename),lang="eng",config='--psm 3',output_type=Output.DICT)
    #extracting conf colomn
    imageconf = result["conf"]
    #removing -1 value which is given to space in sentence
    
    High_average_conf = SpaceValueremoval(imageconf)
    
    #compairing the conf with each language to detect
    High_average_conf3, Detected_lang = CompareLang(High_average_conf, filename) 

    print("tesseract language= ",Detected_lang,"conf= ",High_average_conf3)
    text = pytesseract.image_to_string(Image.open(filename),lang=Detected_lang)
    a, b =langid.classify(text)
    print("Langid language= ",a)
    if a == 'zh':
        lang2 = Detected_lang
    else :
        lang1=pycountry.languages.get(alpha_2=a)
        lang2 = lang1.name
    if lang2 == 'Tagalog':
        lang2 = 'Filipino'
    print(lang2)
    dst_dir = os.path.join(parent_dir, lang2)
    if os.path.exists(dst_dir)== False:
        os.mkdir(dst_dir)
           
    
    #rename the file
    totalFiles = 1
    items = os.listdir(dst_dir)
    for item in items:
        if os.path.isfile(os.path.join(dst_dir, item)):
            totalFiles = totalFiles + 1
    
    e = parent_dir + "\\" + lang2 + str(totalFiles)+ ".png"
    os.rename(src_dir, e)
    print("new name " , e)

    #send the image to destination folder
    for pngfile in glob.iglob(e):
        print("pngfile " , pngfile)
        print("destination Directory copied to" , dst_dir)
        shutil.copy(pngfile, dst_dir)
    
    t1_stop = time.perf_counter()
    print("Elapsed time:", t1_stop - t1_start) # print performance indicator
    
input('Press any key')    
    
