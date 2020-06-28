import string
import random

def generateId(length=11) :
    chars = string.ascii_letters + string.digits
    return [random.choice(chars) for _ in range(length)]

def generetePlaylistId(length=35) :
    chars = string.ascii_letters + string.digits
    return [random.choice(chars) for _ in range(length)]
