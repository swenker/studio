from datetime import datetime
import hashlib
from cms_model import TIME_FORMAT


__author__ = 'wenjusun'


def get_timenow():
    return datetime.now().strftime(TIME_FORMAT)


def encrypt(s):
    return s

def md5(instr):
    return hashlib.md5(instr).hexdigest()