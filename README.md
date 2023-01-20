# Python Watermark
Don't want to release your source code just because you need to add watermarks to your file(s). Python Watermark Allows you to easily add watermarks to PDF, JPG &amp; PNG files with no restrictive licensing

## Installation

Installing the latest PyPI release (recommended)

    python3 -m pip install -U pythonwatermark

This will use a pre-built wheel package, the easiest way of installing pythonwatermark.

## Dependencies

pythonwatermark uses two awesome open source python packages to work it's magic they are...

Pillow - https://github.com/python-pillow/Pillow

Like PIL, Pillow is licensed under the open source HPND License

Pypdfium2 - https://github.com/pypdfium2-team/pypdfium2

PDFium and pypdfium2 are available by the terms and conditions of either Apache-2.0 or BSD-3-Clause, at your choice.

These are both fantastic packages and are liberally licensed meaning unlike with other options you don't need to release your source code to the public.

## Usage
Import watermark utils

    from pythonwatermark import watermarkutils

Add watermark to file

    watermarkutils.put_watermark(inputfile, outputfile, watermark, x=0, y=0, transparency=100, width=None, height=None)
    
#### Required
    
inputfile - path as string to PDF, JPG or PNG you wish to add watermark too

outputfile - path as string to where you want output to be saved with either PDF, JPG or PNG file extension.

watermark - path as string to PDF, JPG or PNG file you are using as your watermark

#### Input/Output

inputfile - can be PDF, JPG or PNG.

outputfile - can be PDF, JPG or PNG if the input file is not a PDF. If the input file is a PDF the output file will either be a PDF or you can pass a folder string and the output will be an image per page in JPG format.

watermark - can be PDF, JPG or PNG. Only PNG supports transparency otherwise the background will be included. If you select a multipage PDF as the watermark it will only take the first page as the image/text to be added as a watermark

#### Optional

x - start point along the x axis for the watermark to be inserted, this can be in PX or "left", "centre" or "right" (if not included x defaults to 0)

y - start point along the y axis for the watermark to be inserted, this can be in PX or "top", "middle" or "bottom" (if not included y defaults to 0)

transparency - the transparency/opacity of the inserted watermark in %. 100% is fully visible 1% is barely visible

width/height - Use one or the other to resize the width/height of the watermark keeping the aspect ratio intact

## Advanced

Use getpxsize to return the size in pixels of a file (input file or watermark for custom positioning)

    w, h = watermarkutils.getpxsize(inputfile)
    
If you are resizing a watermark you can also add either the width/height you are resizing to for more accurate placement on the input file

    w2, h2 = watermarkutils.getpxsize(watermark, width=300)
    w3, h3 = watermarkutils.getpxsize(watermark, height=300)
    
You can use this to work out watermark placement on your input file

    w, h = getpxsize(inputfile)
    w2, h2 = getpxsize(watermark)
    x = int((w / 2) - (w2 / 2))
    y = int((h / 2) - (h2 / 2))
    
This would provide the X & Y to have the watermark positioned in the centre/middle of the page (though we can also achieve this by passing x="centre" & y="middle")
