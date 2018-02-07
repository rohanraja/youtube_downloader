__author__ = 'rohanraja'

from Youlink import Youlink

ylinks = Youlink.objects

# ylinks = [y for y in ylinks if y.checkThumbExists()]

keyFunc = lambda y: y.vidinfo.get('categories', ["Not Mentioned"])[0]

#groups = {}

#for y in ylinks:

    #cat = keyFunc(y)

    #catlist = groups.setdefault(cat, [])
    #catlist.append(y.title)

#print groups


print(len(ylinks))

#for y in ylinks:
    #cat = y.vidinfo.get('categories', "Not Mentioned")

    #if 'Howto & Style' in cat:

        #print y.vidinfo["title"]


from multiprocessing import Pool


def f(id):

    try:
        if (ylinks[id].checkThumbExists()):
            return not ylinks[id].downloadThumb()

    except:
        pass

pool = Pool(processes=15)

result = pool.map(f, list(range(len(ylinks))))

#print result

#
#for y in ylinks:

#     try:
#         y.getVideoDetails()

#     except Exception, e:
#         print "ERROR OCCURRED %s" % e
