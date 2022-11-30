"""
In order to run this correctly, these need to be installed in this order:

pip install numpy
pip install pylibjpeg-openjpeg
pip install opencv
pip install Pillow
pip install pillow_heif


"""

from PIL import Image
import PIL
import os
import openjpeg
import cv2
import numpy as np
import time
import pillow_heif

pillow_heif.register_heif_opener()


def compression_ratio(compressed_image_file_name, original_image_file_name):
    original_image_size = os.stat(original_image_file_name).st_size
    size = os.stat(compressed_image_file_name).st_size
    ratio = original_image_size / size

    return size, ratio


def compress_image(original_image_file_name, file_extension, compression_quality):
    im = Image.open(original_image_file_name)
    rgb_im = im.convert('RGB')
    np_im = np.array(rgb_im)

    compressed_image_file_name = 'Picture.' + file_extension

    start = time.time()
    rgb_im.save(compressed_image_file_name, quality=compression_quality, optimize=True)
    end = time.time()
    compression_time = end - start

    compressed_im = Image.open(compressed_image_file_name)
    compressed_im = compressed_im.convert('RGB')
    compressed_np = np.array(compressed_im)

    psnr = cv2.PSNR(np_im, compressed_np)
    mse = np.square(np.subtract(np_im, compressed_np)).mean()

    compressed_size, c_ratio = compression_ratio(compressed_image_file_name, original_image_file_name)

    results = dict()
    results['MSE'] = mse
    results['PSNR'] = psnr
    results['Compressed Size'] = compressed_size
    results['Compresion Ratio'] = c_ratio
    results['Time'] = compression_time

    return results


# ORIGINAL IMAGE FILE NAME
original_image = "file_example.tiff"

#Lossy
jpg_results = compress_image(original_image, 'jpg', 50)
webp_results = compress_image(original_image, 'webp', 80)
heif_results = compress_image(original_image, 'heif', 50)
gif_results = compress_image(original_image, 'gif', 100)

#Lossless
png_results = compress_image(original_image, 'png', 100)
jpeg2000_results = compress_image(original_image, 'jp2', 100)
tiff_results = compress_image(original_image, 'tiff', 100)


print("JPEG: ", jpg_results)
print("WEBP: ", webp_results)
print("HEIF: ", heif_results)
print("GIF: ", gif_results)
print("PNG: ", png_results)
print("JPEG2000: ", jpeg2000_results)
print("TIFF: ", tiff_results)