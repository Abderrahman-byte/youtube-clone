from django.conf import settings

import os, string, random, subprocess, math
import cv2
from PIL import Image

def generateId(length=11) :
    chars = string.ascii_letters + string.digits
    return ''.join([random.choice(chars) for _ in range(length)])

def generetePlaylistId(length=35) :
    chars = string.ascii_letters + string.digits
    return ''.join([random.choice(chars) for _ in range(length)])

def generateChannelId(length=24) :
    chars = string.ascii_letters + string.digits
    return ''.join([random.choice(chars) for _ in range(length)])

def generateThumbnail(video_name) :
    MEDIA_ROOT = settings.MEDIA_ROOT
    video_path = os.path.join(MEDIA_ROOT, video_name)
    image_id = generateId(30)
    image_path = os.path.join(MEDIA_ROOT, f'images/thumbnails/{image_id}.jpg')

    try :
        video = cv2.VideoCapture(video_path)
        framesTotal = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frameTarget = math.floor(framesTotal * 0.2)
        video.set(1, frameTarget)
        ret, frame = video.read()
        cv2.imwrite(image_path, frame)
    except Exception as ex:
        subprocess.call(['ffmpeg', '-i', video_path, '-r', '1/1440', image_path, "-y"])

    return f'/media/images/thumbnails/{image_id}.jpg'

def randomFileName(instance, filename) :
    id = generateId(30)
    fp, ext = os.path.splitext(filename)
    return f'images/users/{id}{ext}'

def adjustImage(path, w, h) :
    im = Image.open(path)
    im_w, im_h = im.size
    factor = w / h

    if factor == 1 :
        if im_w > im_h :
            box = ((im_w - im_h) / 2, 0, (im_w + im_h) / 2, im_h)
            im = im.crop(box)
        elif im_w < im_h :
            box = (0, (im_h - im_w) / 2, im_w, (im_h + im_w) /2)
            im = im.crop(box)
    elif im_w / factor > im_h and im_h * factor < im_w :
        box = ((im_w - (im_h * factor)) / 2, 0, (im_w + (im_h * factor)) / 2, im_h)
        im = im.crop(box)
    elif im_w / factor < im_h and im_h * factor > im_w :
        box = (0, (im_h - (im_w / factor)) / 2, im_w, (im_h + (im_w / factor)) /2)
        im = im.crop(box)
    
    im = im.resize((w, h))
    im.save(path, quality=1000, subsampling=0)