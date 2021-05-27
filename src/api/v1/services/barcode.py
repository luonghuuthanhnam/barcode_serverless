# !pip install fitz
# !pip install PyMuPDF
# !sudo apt-get install libzbar0
# !pip install pyzbar


from os import name
from PIL import Image
import io
import asyncio

import PIL
import fitz
import numpy as np
from pyzbar import pyzbar
import base64
import time

# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("-pdf_path", "--pdf_path", default = "f1.pdf")
# parser.add_argument("-save_txt_path", "--save_txt_path", default = "barcode.txt")
# args = parser.parse_args()


class BarcodeReader():
    # def __init__(self) -> None:
    #     pass
    def get_image_in_pdf(self, pdf_data)->Image:
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        pix_list = []
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:       # this is GRAY or RGB
                    # pix.writePNG("p%s-%s.png" % (i, xref))
                    pix_list.append(pix)
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    # pix1.writePNG("p%s-%s.png" % (i, xref))
                    pix_list.append(pix1)
                    pix1 = None
                pix = None
        img_list = []
        for p in pix_list:
            arr = p.getImageData()
            stream = io.BytesIO(arr)
            img_list.append(Image.open(stream))
        return img_list
    
    def padding_image(self, image)-> np.array:
        ht, wd, cc= image.shape
        ww = wd+10
        hh = ht+10
        color = (255,255,255)
        result = np.full((hh,ww,cc), color, dtype=np.uint8)

        # compute center offset
        xx = (ww - wd) // 2
        yy = (hh - ht) // 2

        # copy img image into center of result image
        result[yy:yy+ht, xx:xx+wd] = image
        return result

    def __call__(self, pdf_path) -> None:
        img_list = self.get_image_in_pdf(pdf_path)
        padded_image = self.padding_image(np.array(img_list[0]))
        result = pyzbar.decode(padded_image)
        barcode =  result[0].data.decode("utf-8")
        return barcode

async def read_barcode(body, reader):
    start_time = time.time()
    b64string = body
    pdf_data = base64.b64decode(b64string)
    barcode = reader(pdf_data)
    end_time = time.time() - start_time

    # md5_hexdigest, _ = hashing_md5(base64_string, datatype="text")

    out = {
        "time": end_time,
        # "id": md5_hexdigest,
        "value": barcode,
        # "score": score,
    }
    # await asyncio.sleep(1)
    # await asyncio.sleep(0)
    return out

# if __name__ == "__main__":
#     pdf_path = str(args.pdf_path)
#     save_txt_path = str(args.save_txt_path)
#     barcode_reader = BarcodeReader()
#     barcode = barcode_reader(pdf_path)
#     file1 = open(save_txt_path,"w")
#     file1.writelines(barcode)
#     file1.close()
    
        


        