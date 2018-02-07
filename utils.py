__author__ = 'rohanraja'

import urllib.request, urllib.error, urllib.parse

http_proxy  = "http://localhost:8118"
http_proxy  = "http://10.3.100.207:8080"
https_proxy  = "https://10.3.100.207:8080"
http_proxy  = ""
https_proxy  = ""


proxyDict = {
              "http"  : http_proxy,
              "https"  : https_proxy
            }

def download_photo(img_url, file_path = "./test.jpg" ):
    try:
        proxy = urllib.request.ProxyHandler(proxyDict)
        opener = urllib.request.build_opener(proxy)
        urllib.request.install_opener(opener)
        image_on_web = urllib.request.urlopen(img_url)
        if image_on_web.headers.maintype == 'image':
            buf = image_on_web.read()
            downloaded_image = file(file_path, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return False
    except Exception as e:
        print(e)
        return False
    return True

