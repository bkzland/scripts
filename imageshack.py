#!/usr/bin/python

__author__ = "bkzland"
__copyright__ = "Copyright 2013"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "bkzland"
__homepage__ = "github.com/bkzland"
__status__ = "alpha"

__description__ = "Downloads userarchives from imageshack to the current working directory.
Files are sorted by user, server and bucket to avoid collisions, parameter of user is required."

from lxml import html
import json, requests, sys, traceback, urllib, urllib2, posixpath, urlparse, unicodedata, string, os, errno

def download(url, localFileName):
    try:
        req = urllib2.Request(url)
        r = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        if e.code == 404:
            print "URL %s sends 404, download not successful" % url
    
        return False
    else:
        
        f = open(localFileName, 'wb')
        f.write(r.read())
        f.close()
    
    return True

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
    
def main():
    try:
        user = parse_args()
    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
        sys.exit(1)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit(2)

    json_url = "http://imageshack.us/rest_api/v2/images?username=%s&limit=9999&offset=0&hide_empty=true" % user

    print "Fetching imageshack library for user %s" % user
    
    f = urllib.urlopen(json_url)

    is_items = json.loads(f.read().decode("utf-8"))["result"]["images"]
    for is_item in is_items:
        local_directory_path = '%s%s%s%s%s' % (user, os.sep, is_item["server"], os.sep, is_item["bucket"])
        mkdir_p(local_directory_path)
        
        local_file_path = '%s%s%s' % (local_directory_path, os.sep, is_item["filename"])
        remote_file_url = "http://imageshack.com/a/img%d/%d/%s" % (is_item["server"], is_item["bucket"], is_item["filename"])
        
        print "Downloading %s to %s" % (remote_file_url, local_file_path)
        download(remote_file_url, local_file_path)
        
    sys.exit(0)

def parse_args():
    try:
        user=sys.argv[1]
    except IndexError:
        exit("no user?")
    return user
        
if __name__ == "__main__":
    main()

