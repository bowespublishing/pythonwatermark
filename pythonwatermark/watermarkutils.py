import pypdfium2 as pdfium
from PIL import Image
import os
import io

def getpxsize(infile, width=None, height=None):
    infiletype = infile.rsplit('.',1)[1]
    if infiletype.casefold() not in ["pdf","jpg","jpeg","png"]:
        raise ValueError(f"Type {itype} is not supported as an input file. Please use PDF, JPG, JPEG or PNG")
    if infiletype.casefold() == "pdf":
        if height is not None or width is not None:
            doc = pdfium.PdfDocument(infile)
            page = doc.get_page(0)
            docimg = page.render_to(pdfium.BitmapConv.pil_image,scale = 300/72)
            docimg = resize_image(docimg, width, height)
            width, height = docimg.size
        else:
            ps = pdfium.PdfDocument(infile)
            page_size = ps.get_page_size(0)
            width, height = page_size
            width = (width / 72) * 300
            height = (height / 72) * 300
    else:
        inputimage = Image.open(infile)
        if height is not None or width is not None:
            inputimage = resize_image(inputimage, width, height)
        width, height = inputimage.size
        
    return int(width), int(height)
        

def resize_image(resizeimage, width, height):
        if height is None and width is not None:
            height = resizeimage.height * width // resizeimage.width
        elif width is None and height is not None:
            width = resizeimage.width * height // resizeimage.height
        return resizeimage.resize((width, height))

def put_watermark(inputfile, outputfile, watermark, x=0, y=0, transparency=100, width=None, height=None):

    if not os.path.isfile(inputfile):
        raise FileNotFoundError(f"File {inputfile} does not exist.")
    
    if not os.path.isfile(watermark):
        raise FileNotFoundError(f"File {watermark} does not exist.")
    
    itype = inputfile.rsplit('.',1)[1]
    if os.path.isdir(outputfile) == False:
        otype = outputfile.rsplit('.',1)[1]
    else:
        otype = outputfile
    if itype.casefold() not in ["pdf","jpg","jpeg","png"]:
        raise ValueError(f"Type {itype} is not supported as an input file. Please use PDF, JPG, JPEG or PNG")

    if itype.casefold() == "pdf":
        if otype.casefold() != "pdf":
            if not os.path.isdir(outputfile):
                raise FileNotFoundError(f"If you are converting a PDF to JPG the output must be a folder")
    else:

        if otype.casefold() not in ["pdf","jpg","jpeg","png"]:
            raise ValueError(f"Type {otype} is not supported as an output file. Please use PDF, JPG, JPEG or PNG")

    wtype = watermark.rsplit('.',1)[1]
    if wtype.casefold() not in ["pdf","jpg","jpeg","png"]:
        raise ValueError(f"Type {wtype} is not supported as a watermark file. Please use PDF, JPG, JPEG or PNG")
    
    if str(x).casefold() not in ["left","centre","right"]:
        if type(x) != int:
            raise ValueError(f"X should be a number or left/centre/right not {x}.")

    if str(y).casefold() not in ["top","middle","bottom"]:
        if type(y) != int:
            raise ValueError(f"Y should be a number or top/middle/bottom not {y}.")


    if type(transparency) != int:
        raise ValueError(f"Transparency should be a number 0-100 not {transparency}.")
    if transparency < 0 or transparency > 100:
        raise ValueError(f"Transparency should be between 0-100 not {transparency}.")
    
    if type(width) != int and width != None:
        raise ValueError(f"Width should be a number not {width}.")
    if width != None and width <= 1:
        raise ValueError(f"Width should be at least 1 not {width}.")
    
    if type(height) != int and height != None:
        raise ValueError(f"Height should be a number not {height}.")
    if height != None and height <= 1:
        raise ValueError(f"Height should be at least 1 not {height}.")


    if itype.casefold() != "pdf":
        

        image1 = Image.open(inputfile)

        if wtype.casefold() == "pdf":

            doc = pdfium.PdfDocument(watermark)
            page = doc.get_page(0)
            image2 = page.render_to(pdfium.BitmapConv.pil_image,scale = 300/72)
        else:
            image2 = Image.open(watermark)

        if image2.mode!='RGBA':
            alpha = Image.new('L', image2.size, 255)
            image2.putalpha(alpha)

        if height is not None or width is not None:
            image2 = resize_image(image2, width, height)

        if str(x).casefold() == "left":
            x = 0
        elif str(x).casefold() == "centre":
            w, h = getpxsize(inputfile)
            w2, h2 = getpxsize(watermark, width=width, height=height)
            x = int((w / 2) - (w2 / 2))
        elif str(x).casefold() == "right":
            w, h = getpxsize(inputfile)
            w2, h2 = getpxsize(watermark, width=width, height=height)
            x = int(w - w2)

        if str(y).casefold() == "top":
            y = 0
        elif str(y).casefold() == "middle":
            w, h = getpxsize(inputfile)
            w2, h2 = getpxsize(watermark, width=width, height=height)
            y = int((h / 2) - (h2 / 2))
        elif str(y).casefold() == "bottom":
            w, h = getpxsize(inputfile)
            w2, h2 = getpxsize(watermark, width=width, height=height)
            y = int(h - h2)
            


        image2_mask = image2.split()[3].point(lambda i: i * transparency / 100.)
        image1.paste(image2, (x,y), mask=image2_mask)


        image1.save(outputfile)
    elif itype.casefold() == "pdf":
        if wtype.casefold() == "pdf":

            doc = pdfium.PdfDocument(watermark)
            page = doc.get_page(0)
            image2 = page.render_to(pdfium.BitmapConv.pil_image,scale = 300/72)
        else:
            image2 = Image.open(watermark)

        if image2.mode!='RGBA':
            alpha = Image.new('L', image2.size, 255)
            image2.putalpha(alpha)

        if height is not None or width is not None:
            image2 = resize_image(image2, width, height)

        image2_mask = image2.split()[3].point(lambda i: i * transparency / 100.)
            
        imglist =[]
        doc = pdfium.PdfDocument(inputfile)
        page_size = doc.get_page_size(0)

        if str(x).casefold() == "left":
            x = 0
        elif str(x).casefold() == "centre":
            w, h = getpxsize(inputfile)
            w2, h2 = getpxsize(watermark, width=width, height=height)
            x = int((w / 2) - (w2 / 2))
        elif str(x).casefold() == "right":
            w, h = getpxsize(inputfile)
            w2, h2 = getpxsize(watermark, width=width, height=height)
            x = int(w - w2)

        if str(y).casefold() == "top":
            y = 0
        elif str(y).casefold() == "middle":
            w, h = getpxsize(inputfile)
            w2, h2 = getpxsize(watermark, width=width, height=height)
            y = int((h / 2) - (h2 / 2))
        elif str(y).casefold() == "bottom":
            w, h = getpxsize(inputfile)
            w2, h2 = getpxsize(watermark, width=width, height=height)
            y = int(h - h2)

        n_pages = len(doc)
        for i in range(n_pages):
            page = doc.get_page(i)
            image = page.render_to(pdfium.BitmapConv.pil_image,scale = 300/72)
            imglist.append(image)
        for im in range(n_pages):
            imglist[im].paste(image2, (x,y), mask=image2_mask)
        if otype.casefold() == "pdf":
            pdf = pdfium.PdfDocument.new()
            width, height = page_size
            for im in range(n_pages):
                img = pdfium.PdfImageObject.new(pdf)
                faux_file = io.BytesIO()
                imglist[im].save(faux_file, 'jpeg')
                img.load_jpeg(faux_file, autoclose=True)
                matrix = pdfium.PdfMatrix()
                matrix.scale(width, height)
                img.set_matrix(matrix)
                page_image = pdf.new_page(width, height)
                page_image.insert_object(img)
                page_image.generate_content()
            with open(outputfile, "wb") as buffer:
                pdf.save(buffer, version=17)
        else:
            for pic in range(n_pages):
                imglist[pic].save(outputfile + f"page_{pic}.jpg")
