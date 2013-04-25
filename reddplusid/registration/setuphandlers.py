from collective.grok import gs
from reddplusid.registration import MessageFactory as _

@gs.importstep(
    name=u'reddplusid.registration', 
    title=_('reddplusid.registration import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('reddplusid.registration.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
