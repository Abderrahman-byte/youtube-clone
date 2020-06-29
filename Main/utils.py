from django.conf import settings

import os, string, random, subprocess

def generateId(length=11) :
    chars = string.ascii_letters + string.digits
    return ''.join([random.choice(chars) for _ in range(length)])

def generetePlaylistId(length=35) :
    chars = string.ascii_letters + string.digits
    return ''.join([random.choice(chars) for _ in range(length)])

def generateThumbnail(video_name) :
    MEDIA_ROOT = settings.MEDIA_ROOT
    video_path = os.path.join(MEDIA_ROOT, video_name)
    image_id = generateId(30)
    image_path = os.path.join(MEDIA_ROOT, f'images/thumbnails/{image_id}.jpg')

    subprocess.call(['ffmpeg', '-i', video_path, '-r', '1/1440', image_path, "-y"])

    return f'/media/images/thumbnails/{image_id}.jpg'