__author__ = 'Wenju Sun'

import
"""
 This script tries to download given file via http and given the final status summary
"""

MAX_VALUE=10
MIN_VALUE=0
WARN_VALUE=0
CRITICAL_VALUE=0

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3

STATUS_TEXT='OK'
STATUS_CODE=STATE_OK

murl="http://dl-3m.svc.mcitech.cn/items/60/185/3F4CBC95EF6DA685D498CC2090DDE6FB.zip"

def download(url):
    urllib2


