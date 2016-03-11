__author__ = 'abuddenberg'

from gcis_clients.domain import Person

DATASET_IDS = {
    'U.S. Climate Divisional Dataset Version 2': 'nca3-cddv2-r1',
    'World Climate Research Program\'s (WCRP\'s) Coupled Model Intercomparison Project phase 5 (CMIP5) multi-model ensemble': 'nca3-cmip5-r1',
    'World Climate Research Program\'s (WCRP\'s) Coupled Model  Intercomparison Project phase 5 (CMIP5) multi-model ensemble': 'nca3-cmip5-r1',
    'ArboNet': 'cdc-arbonet',
    'U.S. Natural Hazard Statistics': 'noaa-nws-us-natural-hazard-statistics',
    'Billion-Dollar Weather and Climate Disasters': 'noaa-ncdc-billion-dollar-weather-climate-disasters',
    'ESRI USA10 dataset (ArcGIS version 10.0)': 'esri-arcgis-v10-0'
}

COPYRIGHT_TRANSLATIONS = {
    None: None,
    'requested': 'Copyright protected. Obtain permission from the original figure source.',
    'denied': 'Copyright protected. Obtain permission from the original figure source.',
    'obtained': 'Copyright protected. Obtain permission from the original figure source.',
    'original_work_nr': 'Free to use with credit to the original figure source.'
}

PARENT_TRANSLATIONS = {
    'publicationType': 'publication_type_identifier',
    'report_name': 'label',
    'journal_article_title': 'label',
    'book_title': 'label',
    'book_section_title': 'label',
    'conference_proceeding_title': 'label',
    'electronic_article_title': 'label',
    'newspaper_article_title': 'label',
    'web_page_title': 'label'
}

PARENT_PUBTYPE_MAP = {
    'Book': 'book',
    'Book Section': 'report',
    'Conference Proceedings': 'generic',
    'Electronic Article': 'article',
    'Journal Article': 'article',
    'Newspaper Article': 'article',
    'Report': 'report',
    'Web Page': 'webpage'
}

PARENT_SEARCH_HINTS = {
    'report': {
        'Climate Change Impacts in the United States: The Third National Climate Assessment': 'nca3',
        'Third National Climate Assessment': 'nca3',
        'A conceptual framework for action on the social determinants of health': 'conceptual-framework-for-action-on-the-social-determinants-of-health',
        'Regional Surface Climate Conditions in CMIP3 and CMIP5 for the United States: Differences, Similarities, and Implications for the U.S. National Climate Assessment.': 'noaa-techreport-nesdis-144',
        '2012 Census of Agriculture': 'census-agriculture-2012'
    },
    'dataset': {
        'Global Historical Climatology Network - Daily': 'noaa-ncdc-ghcn-daily'
    },
    'article': {
        'Projections of future temperature-attributable deaths in 209 U.S. cities using a cluster based Poisson approach': '10.1186/s12940-015-0071-2',
        'Projections of future temperature-attributable deaths in 209 U.S. cities 1 using a cluster-based Poisson approach': '10.1186/s12940-015-0071-2',
        'A framework for examining climate driven changes to the seasonality and geographic range of coastal pathogens': '10.1016/j.crm.2015.03.002',
        'Effects of Ocean Warming on Growth and Distribution of Five Ciguatera-Associated Dinoflagellates in the Caribbean and Implications for Ciguatera Fish Poisoning': 'potential-effects-of-climate-change-on-growth-and-distribution-of-five-caribbean-gambierdiscus-species',
        'Effects of elevated CO2 on the protein concentration of food crops: a meta-analysis': '10.1111/j.1365-2486.2007.01511.x',
        'A new scenario framework for climate change research: the concept of shared socio-economic pathways': '10.1007/s10584-013-0905-2',
        'Climate Change influences on the annual onset of Lyme disease in the United States': '10.1016/j.ttbdis.2015.05.005',
        'The roads ahead: Narratives for shared socioeconomic pathways describing world futures in the 21st century': '10.1016/j.gloenvcha.2015.01.004'
    },
    'webpage': {
        'Screenshot of: Social Vulnerability Index (SVI) Mapping Dashboard': '6d0ccc19-cdcc-4d56-acb7-d62f12611333',
        'Lyme Disease: Data and Statistics: Maps': '7206f315-04be-4536-9e10-70155edfada0',
        'Risk of very large fires could increase sixfold by mid-century in the US': 'af962cb2-dd38-44f6-9b4e-7bef8577b92c',
        'Flickr account: User: TeamSaintLouis. Album: Low Water on the Mississippi River': '9853a51e-b7c2-42c5-a201-d2f5c8527f52',
        'USDA Biological Control of Pests Research Unit': '950835c0-2088-4f06-a61a-a809387d4930'
    },
    'book': {
        'Assessing Health Vulnerability to Climate Change: A Guide for Health Departments': ('report', 'assessing-health-vulnerability-to-climate-change-a-guide-for-health-departments')
    }
}

ORG_IDS = {
    'NOAA NCDC/CICS-NC': 'cooperative-institute-climate-satellites-nc',
    'NCDC/CICS-NC': 'cooperative-institute-climate-satellites-nc',
    'NOAA NCDC/CICS NC': 'cooperative-institute-climate-satellites-nc',
    'NESDIS/NCDC': 'national-climatic-data-center',
    'NCDC': 'national-climatic-data-center',
    'U.S. Forest Service': 'us-forest-service',
    'NOAA Pacific Marine Environmental Laboratory': 'pacific-marine-environmental-laboratory',
    'Jet Propulsion Laboratory': 'jet-propulsion-laboratory',
    'HGS Consulting': 'hgs-consulting-llc',
    'University of Virginia': 'university-virginia',
    'Miami-Dade Dept. of Regulatory and Economic Resources': 'miami-dade-dept-regulatory-economic-resources',
    'Nansen Environmental and Remote Sensing Center': 'nansen-environmental-and-remote-sensing-center',
    'University of Illinois at Urbana-Champaign': 'university-illinois',
    'USGCRP': 'us-global-change-research-program',
    'National Park Service': 'national-park-service',
    'Institute of the Environment': 'university-arizona',
    'USGS': 'us-geological-survey',
    'University of Puerto Rico': 'university-puerto-rico',
    'University of Alaska': 'university-alaska',
    'U.S. Department of Agriculture': 'us-department-agriculture',
    'Kiksapa Consulting': 'kiksapa-consulting-llc',
    'Centers for Disease Control and Prevention': 'centers-disease-control-and-prevention',
    'Pacific Northwest Laboratories': 'pacific-northwest-national-laboratory',
    'Susanne Moser Research & Consulting': 'susanne-moser-research-consulting',
    'NEMAC': 'national-environmental-modeling-analysis-center',
    'LBNL': 'lawrence-berkeley-national-laboratory',
    'Texas Tech University': 'texas-tech-university',
    'Centers for Disease Control and Prevention / National Center for Atmospheric Research': 'centers-disease-control-and-prevention',
    'Stratus Consulting Inc.': 'stratus-consulting'
}

# host
# point_of_contact
# editor
# analyst
# principal_author
# secondary_author
# data_producer
# author
# scientist
# coordinator
# manager
# convening_lead_author
# lead_author
# contributor
# lead_agency
# publisher
# executive_editor
# distributor
# engineer
# primary_author
# graphic_artist
# coordinating_lead_author
# contributing_editor
# funding_agency
# contributing_author
# data_archive
# advisor
# contributing_agency

PERSON_TRANSLATIONS = {
    'Alexis St. Juliana': Person({'id': 9934, 'first_name': 'Alexis', 'last_name': 'St. Juliana'}),
    'Alexis Juliana': Person({'id': 9934, 'first_name': 'Alexis', 'last_name': 'St. Juliana'}),
    'Pat Dolwick': Person({'first_name': 'Patrick', 'last_name': 'Dolwick'}),
    'Alan Joyner': Person({'first_name': 'Alan', 'last_name': 'Joyner'}),
    'Juli Trtanj': Person({'id': 1264, 'first_name': 'Juli M.', 'last_name': 'Trtanj'}),
    'Juli M. Trtanj': Person({'id': 1264, 'first_name': 'Juli M.', 'last_name': 'Trtanj'}),
    'Stephanie Moore': Person({'id': 9889, 'first_name': 'Stephanie K.', 'last_name': 'Moore'}),
    'Stephanie K. Moore': Person({'id': 9889, 'first_name': 'Stephanie', 'last_name': 'Moore'}),
    'Steve Kibler': Person({'first_name': 'Steven R.', 'last_name': 'Kibler'}),
    'Jesse Bell': Person({'first_name': 'Jesse E.', 'last_name': 'Bell'}),
    'Dave Mills': Person({'first_name': 'David M.', 'last_name': 'Mills'}),
    'David Mills': Person({'first_name': 'David M.', 'last_name': 'Mills'}),
    'Lesley Crimmins)': Person({'first_name': 'Lesley', 'last_name': 'Jantarasami'}),
    'Allison Jantarasami)': Person({'first_name': 'Allison', 'last_name': 'Crimmins'}),
    'Lewis Ziska': Person({'id': 923, 'first_name': 'Lewis', 'last_name': 'Ziska'}),
    'Jada Garofalo': Person({'id': 9885, 'first_name': 'Jada', 'last_name': 'F. Garofalo'}),
    'Micah Hahn': Person({'id': 9886, 'first_name': 'Micah', 'last_name': 'Hahn'}),
    'Jeanette Thurston': Person({'id': 9892, 'first_name': 'Jeanette', 'last_name': 'Thurston'}),
    'Daniel Dodgen': Person({'id': 9908, 'first_name': 'Daniel', 'last_name': 'Dodgen'}),
    'John Jacobs': Person({'id': 9888, 'first_name': 'John', 'last_name': 'Jacobs'}),
    'Stephanie Herring': Person({'id': 8333, 'first_name': 'Stephanie', 'last_name': 'Herring'}),
    'Tom Maycock': Person({'id': 10926, 'first_name': 'Tom', 'last_name': 'Maycock'})
}

CONTRIB_ROLES = {
    'Kenneth Kunkel': ('cooperative-institute-climate-satellites-nc', 'scientist'),
    'Allison Crimmins': ('us-environmental-protection-agency', 'point_of_contact'),
    'Micah Hahn': ('centers-disease-control-and-prevention', 'scientist'),
    'Jada Garofalo': ('centers-disease-control-and-prevention', 'point_of_contact'),
    'Ben Beard': ('centers-disease-control-and-prevention', 'scientist'),
    'Dave Mills': ('stratus-consulting', 'analyst'),
    'David Mills': ('stratus-consulting', 'analyst'),
    'Alexis Juliana': ('stratus-consulting', 'analyst'),
    'Alexis St. Juliana': ('stratus-consulting', 'analyst'),
    'Neal Fann': ('us-environmental-protection-agency', 'analyst'),
    'Pat Dolwick': ('us-environmental-protection-agency', 'scientist'),
    'Lewis Ziska': ('us-department-agriculture', 'scientist'),
    'Juli Trtanj': ('national-oceanic-atmospheric-administration', 'point_of_contact'),
    'Alan Joyner': ('university-north-carolina-chapel-hill', 'graphic_artist'),
    'Jeanette Thurston': ('us-department-agriculture', 'scientist'),
    'Richard Streeter': ('stratus-consulting', 'analyst'),
    'Stephanie Moore': ('national-oceanic-atmospheric-administration', 'scientist'),
    'Steve Kibler': ('national-oceanic-atmospheric-administration', 'scientist'),
    'Jesse Bell': ('national-oceanic-atmospheric-administration', 'scientist'),
    'Lesley Jantarasami': ('us-environmental-protection-agency', 'analyst'),
    'Daniel Dodgen': ('us-department-health-human-services', 'point_of_contact'),
    'Andrea Maguire': ('us-environmental-protection-agency', 'point_of_contact'),
    'Lesley Crimmins)': ('us-environmental-protection-agency', 'analyst'),
    'Allison Jantarasami)': ('us-environmental-protection-agency', 'point_of_contact'),
    'John Jacobs': ('national-oceanic-atmospheric-administration', 'scientist'),
    'Stephanie Herring': ('national-oceanic-atmospheric-administration', 'scientist'),
    'Tom Maycock': ('cooperative-institute-climate-satellites-nc', 'point_of_contact'),
}
