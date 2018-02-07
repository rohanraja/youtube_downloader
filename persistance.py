from peewee import *
import config

db = SqliteDatabase(config.getDBDir())

# db = PostgresqlDatabase('youlinks', user='rraja')

class Youlink(Model):
    url = CharField()
    path = CharField()
    state = CharField()
    category = CharField()

    class Meta:
        database = db # This model uses the "people.db" database.

def getYoulinkById(idd):
    ylink = Youlink.select().where(Youlink.id == idd)
    return ylink[0]
    
def getYoulinkByURL(url):
    ylink = Youlink.select().where(Youlink.url == url)
    return ylink[0]

def saveLink(url, title='', folder=''):

    with db.transaction():
        Youlink.create(url=url, path=title, state="new", category=folder)

def checkIfAlreadyDone(url):

    ylink = Youlink.select().where(Youlink.url == url)
    return len(ylink) > 0

def checkIfUnfinished(url):
    ylink = Youlink.select().where(Youlink.url == url)
    return ylink[0].state != "done"

def setState(url, state):

    query = Youlink.update(state=state).where(Youlink.url == url)
    query.execute()

def markProcessing(url):
    setState(url, "processing")

def markFinished(url):
    setState(url, "done")


def getUnfinished():
    ylinks = Youlink.select().where(Youlink.state != "done")
    return ylinks

def getAll():
    ylinks = Youlink.select()
    return ylinks


if __name__ == "__main__":
    # setState("3434", "done")
    # print checkIfAlreadyDone("3sd434")
    db.connect()
    db.create_tables([Youlink])
