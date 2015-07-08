__author__ = 'abuddenberg'

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

PARENT_SEARCH_HINTS = {}

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
    'Texas Tech University': 'texas-tech-university'
}

CONTRIB_ROLES = {
    'Kenneth Kunkel': 'scientist',
    'Xungang Yin': 'scientist',
    'Nina Bednarsek': 'scientist',
    'Henry Schwartz': 'scientist',
    'Jessicca Griffin': 'graphic_artist',
    'James Youtz': 'scientist',
    'Chris Fenimore': 'scientist',
    'Deb Misch': 'graphic_artist',
    'James Galloway': 'scientist',
    'Laura Stevens': 'scientist',
    'Nichole Hefty': 'point_of_contact',
    'Mike Squires': 'scientist',
    'Peter Thorne': 'scientist',
    'Donald Wuebbles': 'scientist',
    'Felix Landerer': 'scientist',
    'David Wuertz': 'scientist',
    'Russell Vose': 'scientist',
    'Gregg Garfin': 'scientist',
    'Jeremy Littell': 'scientist',
    'Emily Cloyd': 'contributing_author',
    'F. Chapin': 'scientist',
    ' Chapin': 'scientist',
    'Andrew Buddenberg': 'analyst',
    'Jerry Hatfield': 'author',
    'George Luber': 'lead_author',
    'Kathy Hibbard': 'lead_author',
    'Susanne Moser': 'convening_lead_author',
    'Bull Bennett': 'convening_lead_author',
    'Ernesto Weil': 'scientist',
    'William Elder': 'scientist',
    'Greg Dobson': 'analyst',
    'Michael Wehner': 'scientist',
    'Katharine Hayhoe': 'scientist'
}
