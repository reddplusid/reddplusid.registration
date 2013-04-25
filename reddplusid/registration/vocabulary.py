from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource
from Products.CMFCore.utils import getToolByName


class BaseVocabularyFactory(grok.GlobalUtility):
    grok.baseclass()
    grok.implements(IVocabularyFactory)
    terms = []

    def __call__(self, context):
        terms = []
        for item in self.terms:
            terms.append(SimpleTerm(**item))
        return SimpleVocabulary(terms)

class Category(BaseVocabularyFactory):
    grok.name('reddplusid.registration.category')

    terms = [{
        'title': 'Government',
        'value': 'government'
    },{
        'title': 'Multilateral / Bilateral',
        'value': 'multilateral-bilateral'
    },{
        'title': 'IFI',
        'value': 'ifi',
    },{
        'title': 'CSO',
        'value': 'cso'
    },{
        'title': 'Private Sector',
        'value': 'private-sector',
    },{
        'title': 'Academia/Education',
        'value': 'academia-education',
    },{
        'title': 'Consultant',
        'value': 'consultant'
    }]

class Gender(BaseVocabularyFactory):
    grok.name('reddplusid.registration.gender')

    terms = [{
        'title': 'Male',
        'value': 'male'
    },{
        'title': 'Female',
        'value': 'female',
    }]

class AgeGroup(BaseVocabularyFactory):
    grok.name('reddplusid.registration.age_group')

    terms = [{
        'title':'< 24',
        'value': '0-24',
    },{
        'title':'25-35',
        'value':'25-35',
    },{
        'title':'36-45',
        'value':'36-45'
    },{
        'title':'46-55',
        'value':'46-55',
    },{
        'title':'> 56',
        'value':'56+'
    }]

class Expertise(BaseVocabularyFactory):
    grok.name('reddplusid.registration.expertise')

    terms = [{
        'title':'Mapping and GIS',
        'value':'mapping-and-gis'
    },{
        'title':'Funding Instruments',
        'value':'funding-instruments',
    },{
        'title':'Projects Management',
        'value':'project-management',
    },{
        'title':'Legislation and Law Enforcement',
        'value':'legislation-and-lawenforcement'
    },{
        'title':'Knowledge Management and Support',
        'value':'knowledgemanagement-and-support',
    },{
        'title':'Monitoring, Reporting and Verification (MRV)',
        'value':'monitoring-reporting-and-verification'
    },{
        'title':'Clean Development Strategies and Planning',
        'value':'clean-development-strategies-and-planning',
    },{
        'title':'Communications and Stakeholder Engagement',
        'value':'communications-and-stakeholderengagement'
    }]
