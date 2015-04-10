__author__ = 'abuddenberg'

from gcis_clients import GcisClient, SurveyClient, survey_token, gcis_dev_auth
from gcis_clients.domain import Report, Chapter

from collections import OrderedDict

gcis = GcisClient('http://data.gcis-dev-front.joss.ucar.edu', *gcis_dev_auth)
surveys = SurveyClient('https://healthresources.globalchange.gov', survey_token)

sync_metadata_tree = {
    'usgcrp-climate-and-health-assessment-draft': OrderedDict([
        ('executive-summary', []),
        ('climate-change-and-human-health', []),
        ('temperature-related-death-and-illness', []),
        ('air-quality-impacts', []),
        ('vectorborne-diseases', []),
        ('water-related-illnesses', []),
        ('food-safety--nutrition--and-distribution', []),
        ('extreme-weather', []),
        ('mental-health-and-well-being', []),
        ('populations-of-concern', []),
        ('appendix-1--technical-support-document', [])

    ])
}

survey_list = surveys.get_list()
for i, survey in enumerate(survey_list):
    url = survey['url']
    print 'Processing: {url} ({i}/{total})'.format(url=url, i=i + 1, total=len(survey_list))

    s = surveys.get_survey(url)
    if s:
        print s.identifier



def create_health_report():
    hr = Report({})
    hr.identifier = 'usgcrp-climate-and-health-assessment-draft'
    hr.report_type_identifier = 'assessment'
    hr.title = 'Impacts of Climate Change on Human Health in the United States: A Scientific Assessment'
    hr.url = 'http://www.globalchange.gov/health-assessment'
    hr.publication_year = '2015'
    hr.contact_email = 'healthreport@usgcrp.gov'

    # ['report_identifier', 'identifier', 'number', 'title', 'url']
    chapters = [
        ('executive-summary', None, 'Executive Summary'),
        ('climate-change-and-human-health', 1, 'Climate Change and Human Health'),
        ('temperature-related-death-and-illness', 2, 'Temperature-Related Death and Illness'),
        ('air-quality-impacts', 3, 'Air Quality Impacts '),
        ('vectorborne-diseases', 4, 'Vectorborne Diseases'),
        ('water-related-illnesses', 5, 'Climate Impacts on Water-Related Illnesses'),
        ('food-safety--nutrition--and-distribution', 6, 'Food Safety, Nutrition, and Distribution'),
        ('extreme-weather', 7, 'Impacts of Extreme Events on Human Health'),
        ('mental-health-and-well-being', 8, 'Mental Health and Well-Being'),
        ('populations-of-concern', 9, 'Climate-Health Risk Factors and Populations of Concern'),
        ('appendix-1--technical-support-document', None, 'Appendix 1: Technical Support Document')
    ]

    # print gcis.create_report(hr)

    for id, num, title in chapters:
        ch = Chapter({})
        ch.identifier = id
        ch.number = num
        ch.title = title
        ch.report_identifier = hr.identifier

        print gcis.create_chapter(hr.identifier, ch)