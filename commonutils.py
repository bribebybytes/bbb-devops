from  ytutils import inityt
from  ytutils import extractthumbnails


def image_paste_over (layer1_img, layer2_img):
    print ("inside image_paste_over")
    youtube = init_yt()
    print(youtube)
    extract_thumbnails(youtube)


def main():
    print ("calling main")
    layer1_img = ""
    layer2_img = ""
    print ("calling image_paste_over")
    image_paste_over (layer1_img, layer2_img)