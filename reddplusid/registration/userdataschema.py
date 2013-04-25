from zope.interface import implements
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from plone.app.users.browser.personalpreferences import UserDataPanel, UserDataConfiglet
from plone.app.users.browser.register import RegistrationForm
from zope import schema
from zope.component import getUtility
from zope.formlib.widget import BrowserWidget
from Products.CMFCore.utils import getToolByName

class DisplayWidget(BrowserWidget):

    def __init__(self, context, request):
        super(DisplayWidget, self).__init__(context, request)
        self.required = False


    def __call__(self):
        if self._renderedValueSet():
            value = self._data
        else:
            value = self.context.default
        if value == self.context.missing_value:
            return ""
        return value


COC=u'''
            <h2>Code of Conduct</h2>

          <div style="overflow: auto; border: 1px solid; padding: 5px; width:
              500px; height: 300px; background: #FFFFE3">



            <p>
            We want all members to have a safe, interesting and friendly
            user experience. Accordingly, all users of the REDD+ Management Centre and any
            contributions they make to the REDD+ Management Centre must comply with this Code of
            Conduct. Your use of the REDD+ Management Centre means that you accept and agree to abide
            by this Code of Conduct.  </p>
            <p>
            We may need to revise the Code of Conduct from time to time by
            amending this page.  Users will be notified of any changes by a
            notice on the website.  However, please review this page
            regularly to ensure you are aware of any changes.  </p>
            <p>
            If you reasonably believe that any contribution to the REDD+ Management Centre made by
            another user contravenes this Code of Conduct, please notify REDD+
            Management Centre.
            Within this Code of Conduct, "contribution" means any material
            posted or uploaded to the REDD+ Management Centre by a member e.g. text, files, documents,
            presentations, photographs, graphics, video or audio material.
            </p>
            <p>
            <b>
            Your contributions must not:
            </b>
            </p>
            <ul>
                <li>
                contain unlawful or objectionable content nor involve disruptive, offensive or abusive behavior. Please be respectful and civil to other members, even if you disagree with them.
                </li>
                <li>
                infringe on anyone else's rights, including copyright i.e. including trade marks, database, trade secret, privacy, publicity, personal or proprietary rights of any kind.
                </li>
                <li>
            contain unsuitable or irrelevant website addresses or URLs  i.e. links to inappropriate content will be removed.
            </li>
            <li>
            promote illegal or anti-social behavior i.e. contributions must not contain violent or sexually explicit material or advocate, promote or assist any unlawful act e.g. terrorist acts, copyright infringement or computer misuse.
            </li>
            <li>
            misrepresent their origins i.e. contributions and/or user names may not be used to impersonate any other person, to misrepresent your identity or affiliation with any person or organization. Impersonating another user whilst online may result in membership exclusion
            </li>
            <li>
            involve any flooding, spamming or advertising.
            </li>
            </ul>
        </div>
'''

def validateAccept(value):
    if not value == True:
        return False
    return True

class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """

    category = schema.Choice(title=u'User Category',
                description=u'Select Category you belong to',
                vocabulary='reddplusid.registration.category')

    organization = schema.TextLine(title=u'Organization/Department',
        description=u'Enter your organization/department',
    )

#    region = schema.Choice(title=u'Geographical location',
#        vocabulary='reddplusid.registration.region'
#    )

    jobtitle = schema.TextLine(title=u'Job Title',
                description=u'Enter your job title',
                required=False)

    gender = schema.Choice(title=u'Gender',
        vocabulary='reddplusid.registration.gender',
        required=False
    )

    age_group = schema.Choice(title=u'Age Group',
        vocabulary='reddplusid.registration.age_group',
        required=False
    )


    expertise = schema.List(title=u'Areas of Your Expertise',
                description=(
                    u'Select up to three REDD + ' + 
                    u'thematic areas of expertise '),
                value_type=schema.Choice(
                    vocabulary=u'reddplusid.registration.expertise'
                ),
                max_length=3)

    skypeid = schema.TextLine(title=u'Skype ID',
                description=u'Enter your skype id',
                required=False)


    conduct_text = schema.Text(readonly=True, default=COC)

    conduct = schema.Bool(
        title=u'Yes I agree to abide by the REDD+ Management Centre Code of Conduct.',
        description=u'''Please click on the check box above if you agree with
                        the Code of Conduct.''',
        constraint=validateAccept)

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return IEnhancedUserDataSchema

def prop(name, default):
    def getter(self):
        return self.context.getProperty(name, default)

    def setter(self, value):
        return self.context.setMemberProperties({name: value})

    return property(getter, setter)

class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    implements(IEnhancedUserDataSchema)

    category = prop('category', '')
    organization = prop('organization', '')
    jobtitle = prop('jobtitle', '')
    gender = prop('gender','')
    age_group = prop('age_group', '')
    expertise = prop('expertise', []) 
    skypeid = prop('skypeid', '')

    def _get_conduct_text(self):
        return COC
    def _set_conduct_text(self, value):
        pass
    conduct_text = property(_get_conduct_text, _set_conduct_text)

    def _get_conduct(self):
        return self.context.getProperty('conduct', '').lower() == 'agree'
    def _set_conduct(self, value):
        self.context.setMemberProperties({'conduct': 'agree' if value else ''})
    conduct = property(_get_conduct, _set_conduct)


class CustomizedUserDataPanel(UserDataPanel):
    def __init__(self, context, request):
        super(CustomizedUserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.select(
                'fullname', 'email', 'category',
                'organization', 'gender','age_group',
                'jobtitle', 'skypeid', 'expertise',
                'description', 'portrait', 'pdelete', 
                'conduct_text', 'conduct')
        self.form_fields['conduct_text'].custom_widget = DisplayWidget

    def _on_save(self, data=None):
        mt = getToolByName(self.context, 'portal_membership')
        member = mt.getAuthenticatedMember()
        portal_url = self.context.absolute_url()
        self.request.response.redirect(
            '%s/author/%s' % (portal_url, member.getId())
        )



class CustomizedUserDataConfiglet(UserDataConfiglet):
    def __init__(self, context, request):
        super(CustomizedUserDataConfiglet, self).__init__(context, request)
        self.form_fields = self.form_fields.select(
                'fullname', 'email', 'category',
                'organization', 'gender','age_group',
                'jobtitle', 'skypeid', 'expertise',
                'description', 'portrait', 'pdelete',
                'conduct_text', 'conduct')
        self.form_fields['conduct_text'].custom_widget = DisplayWidget


#    def _on_save(self, data=None):
#        mt = getToolByName(self.context, 'portal_membership')
#        userid = context.REQUEST.form.get('userid')
#        member = mt.getMemberById(userid)


class CustomizedRegistrationForm(RegistrationForm):
    
    @property
    def form_fields(self):
        fields = super(CustomizedRegistrationForm, self).form_fields
        fields['conduct_text'].custom_widget = DisplayWidget
        return fields
