from processUrl import processVLCUrl

def addUrl(url, cat):

    processVLCUrl.apply_async(args=[url, cat], queue="processVLCUrl")

if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    cat = sys.argv[2]
    addUrl(url, cat)
