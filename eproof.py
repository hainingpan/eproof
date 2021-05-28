from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import base64
import numpy as np

def shift_image(src_image,dst_image,direction,color,transparency=100):
    '''
    direction=[up,down] moves
    color= np.array([0,0,255])
    '''
    dx=[]
    dy=[]
    dxy=np.argwhere((src_image==color).all(axis=2))
    dx=dxy[:,0]
    dy=dxy[:,1]
    mat=np.zeros((src_image.shape[0],src_image.shape[1]),dtype=int)
    mat[dx,dy]=1
    mat_upward=np.array([np.roll(mat,-(i+1),0) for i in range(direction[0])])
    mat_downward=np.array([np.roll(mat,(i+1),0) for i in range(direction[1])])
    mat_final=mat_upward.sum(axis=0)+mat_downward.sum(axis=0)+mat
    dx2,dy2=np.nonzero(mat_final)
    dst_image[dx2,dy2]=np.array(color+[transparency])
    dst_image[dx,dy]=np.array(color+[255])
    dst_image[dx2,100:120]=np.array(color+[255])

def image_proc(original_img_data):
    im = Image.open(BytesIO(base64.b64decode(original_img_data)))
    imagedata=(np.array(im))
    # imagedata2=255*np.ones((imagedata.shape[0],imagedata.shape[1],imagedata.shape[2]+1))
    imagedata2=np.concatenate([imagedata,255*np.ones((imagedata.shape[0],imagedata.shape[1],1))],axis=2)

    shift_image(imagedata,imagedata2,[8,9],[255,0,0])
    shift_image(imagedata,imagedata2,[20,0],[0,0,255])
    shift_image(imagedata,imagedata2,[0,0],[255,255,0])

    new_img=Image.fromarray(np.uint8(imagedata2))

    output = BytesIO()
    new_img.save(output, format='PNG')
    new_img_data = output.getvalue()
    
    new_img_encode = base64.b64encode(new_img_data)
    if not isinstance(new_img_encode, str):
        # Python 3, decode from bytes to string
        new_img_encode = new_img_encode.decode()
    new_img_url = 'data:image/jpg;base64,' + new_img_encode
    return new_img_url

def read_html():
    print('type HTML filename:')
    filename=input()
    with open(filename, 'r') as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    imgtext_list=soup.find_all('img')[:-1]
    for index,imgtext in enumerate(imgtext_list):
        print('Processing Page {:d}/{:d}...'.format(index+1,len(imgtext_list)))
        original_img_data=imgtext['src']
        original_img_data=original_img_data.replace('data:image/png;base64,','')
        new_img_data=image_proc(original_img_data)
        imgtext['src']=new_img_data
    with open(filename.replace('.html','_mod.html'),'w',encoding='utf-8') as f:
        f.write(str(soup))

if __name__=="__main__":
    read_html()
