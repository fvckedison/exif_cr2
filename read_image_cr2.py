import glob
import os
import exifread
from PIL import Image
import skimage
import rawpy
import imageio
import numpy as np
from rawkit.raw import Raw

def get_exif(img_file):
    f = open(img_file, 'rb')
    tags = exifread.process_file(f)
    
    result = []
    for k in tag_names:
        result.append(str(tags[k]))
    
    f.close()
    return result

tag_names = ['Image ImageWidth', 'Image ImageLength', 'Image Model', 'Image DateTime'
        , 'EXIF ExposureTime', 'EXIF FNumber', 'EXIF ExposureProgram'
        , 'EXIF ISOSpeedRatings', 'EXIF FocalLength']


header = '序號,照片名稱,濾鏡,拍攝日期,拍攝地點,品系,影像寬,影像長,相機,拍攝時間,曝光時間,光圈孔徑,曝光程式,ISO速度,焦距,拍攝範圍,得病狀況,植株編號,拍攝方式'

in_dir =r'C:\Users\Edison Lien\Desktop\IL720-0312LC-E240'

out_file = 'VL-0312LC.csv'

fp = open(out_file, 'w')
fp.write('%s\n' % header)

f_list = glob.glob(in_dir + '*')
img_folder=out_file[:-4] + '_resize'
os.mkdir(img_folder)
count = 1
for f in f_list:
    print(f_list)
    if os.path.isdir(f):
        s = f.replace('\\', '/')
        print('reading files in: ', s)
        
        s2 = s.split('/')
        s3 = s2[-1].split('-')
        print(s3)
        lens = s3[0]
        dt = '2021' + s3[1][:4]
        place = s3[1][4:]
        species = s3[2]
        print(lens, dt, place, species)
        img_list = glob.glob('{}/*.CR2'.format(s))
        for img in img_list:
            f = open(img, 'rb')
            tags = exifread.process_file(f) 
            if os.path.isfile(img):
                exif_data = get_exif(img)
                exif_str = ','.join(exif_data)
                width= int(str(tags['Image ImageWidth']))
                height= int(str(tags['Image ImageLength']))
                new_w = int(width / 10)
                new_h = int(height / 10)
                basename = os.path.basename(img)
                image_name = basename[:-4]
                path_s=str(img)
                path=path_s.replace("\\","/")
                raw = rawpy.imread(img)
                rgb = raw.postprocess()
                save_path=img_folder+"/"+ image_name+".tiff"
                imageio.imsave(save_path,rgb)
                im=Image.open(save_path)
                
                
                img_resize = im.resize((new_w, new_h))
                img_resize.save(img_folder+"/"+ image_name+"_resize.tiff") 

                #print('image file: ', image_name)
                
                data = '{},{},{},{},{},{},{}'.format(count,image_name,lens,dt,place,species,exif_str)
                fp.write('%s\n' % data)
                
                count += 1
                
fp.close()
print('*** done ***')