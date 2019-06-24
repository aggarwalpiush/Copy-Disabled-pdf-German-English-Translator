#! usr/bin env python
# -*- coding : utf-8 -*-


from wand.image import Image
from PIL import Image as img
import pytesseract
import cv2
import os
import codecs
import sys
import translator.txt2pdf as tp
from googletrans import Translator
from PyPDF2 import PdfFileMerger


class PdfToImage(object):
    def __init__(self):
        pass

    def convert_pdftojpg(self, pdf_path):
        myimage = []
        with Image(filename=pdf_path) as img:

            with img.convert('png') as converted:
                converted.save(filename='../data/page.png')
            for i in range(len(img.sequence)):
                myimage.append('page-'+str(i)+'.png')
        return myimage

    def convert_jpgtotext(self,images):
        # load the example image and convert it to grayscale
        text_file = []
        for i in images:
            image = cv2.imread('../data/'+str(i))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # write the grayscale image to disk as a temporary file so we can
            # apply OCR to it
            filename = "{}.png".format(i)
            cv2.imwrite(filename, gray)
            # save
            text = pytesseract.image_to_string(img.open(filename))
            os.remove(filename)
            os.remove('../data/'+str(i))
            with codecs.open('../data/'+str(i)+'.txt', 'w', 'utf-8') as textfile:
                textfile.write(text)
                text_file.append('../data/'+str(i)+'.txt')
        return text_file

    def convert_l1tol2(self, src_path, tgt_lang):
        target_path = []
        translator = Translator()
        for sf in src_path:
            input_translate = []
            with codecs.open(sf, 'r', 'utf-8') as spath:
                for line in spath:
                    input_translate.append(line)
            output_translations = translator.translate(input_translate, dest=tgt_lang)
            with codecs.open(str(sf) + '.en', 'w', 'utf-8') as tpath:
                for translation in output_translations:
                    tpath.write(str(translation.text)+'\n')
            target_path.append(str(sf)+'.en')
            os.remove(sf)
        return target_path

    def convert_texttopdf(self, src_path):
        pdf_path = []
        for i in src_path:
            pc = tp.PDFCreator(i, str(i)+'.pdf')
            pc.generate()
            pdf_path.append(str(i)+'.pdf')
            #os.remove(i)
        return pdf_path

    def merge_pdf(self,src_path, output_path):
        merger = PdfFileMerger()

        for pdf in src_path:
            merger.append(open(pdf, 'rb'))
            #os.remove(pdf)

        with open(output_path, 'wb') as fout:
            merger.write(fout)


def main():
    pi = PdfToImage()
    images = pi.convert_pdftojpg('/Users/piaggarwal/Recommender System/Folien - Uebung 10.pdf')
    textfiles = pi.convert_jpgtotext(images)
    pdfs_orig = pi.convert_texttopdf(textfiles)
    pi.merge_pdf(pdfs_orig, '../data/orig_output.pdf')
    translatedtext = pi.convert_l1tol2(textfiles, 'en')
    pdfs = pi.convert_texttopdf(translatedtext)

    pi.merge_pdf(pdfs, '../data/translated_output.pdf')


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()









