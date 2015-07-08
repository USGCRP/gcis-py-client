__author__ = 'abuddenberg'

FIG_TRANSLATIONS = {
    'what_is_the_figure_id': 'identifier',
    'what_is_the_name_of_the_figure_as_listed_in_the_report': 'title',
    'when_was_this_figure_created': 'create_dt',
    'what_is_the_chapter_and_figure_number': 'figure_num'
}

IMG_TRANSLATIONS = {
    'list_any_keywords_for_the_image': 'attributes',
    'when_was_this_image_created': 'create_dt',
    'what_is_the_image_id': 'identifier',
    'maximum_latitude': 'lat_max',
    'minimum_latitude': 'lat_min',
    'maximum_longitude': 'lon_max',
    'minimum_longitude': 'lon_min',
    'start_time': 'time_start',
    'end_time': 'time_end',
    'what_is_the_name_of_the_image_listed_in_the_report': 'title'
}

DATASET_TRANSLATIONS = {
    'data_set_access_date': 'access_dt',
    'data_set_publication_year': 'publication_year',
    'data_set_original_release_date': 'release_dt',
    # HACK elsewhere 'start_time and end_time': '',
    'data_set_id': 'native_id',
    # HACK elsewhere'': 'doi',
    # HACK elsewhere 'maximum_latitude etc. etc. etc.': '',
    'data_set_version': 'version',
    'data_set_name': 'name',
    'data_set_citation': 'cite_metadata',
    'data_set_description': 'description',
    # Not sure'': 'type',
    'data_set_location': 'url',
    'data_set_variables': 'attributes'
}

ACT_TRANSLATIONS = {
    'how_much_time_was_invested_in_creating_the_image': 'duration',
    '35_what_are_all_of_the_files_names_and_extensions_associated_with_this_image': 'output_artifacts',
    'what_operating_systems_and_platforms_were_used': 'computing_environment',
    'what_analytical_statistical_methods_were_employed_to_the_data': 'methodology',
    'describe_how_the_data_was_used_in_the_image_figure_creation': 'data_usage',
    'list_the_name_and_version_of_the_software': 'software',
    'what_software_applications_were_used_to_manipulate_the_data': 'notes',
    '33_what_software_applications_were_used_to_visualize_the_data': 'visualization_software'

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
    'NASA': 'national-aeronautics-space-administration',
    'GATech': 'georgia-institute-technology',
    'UW': 'university-washington'
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
    'Katharine Hayhoe': 'scientist',
    'Walt Meier': 'scientist',
    'Aris Georgakakos': 'scientist',
    'Matthew Peters': 'scientist',
    'Robert Norheim': 'scientist'
}

PARENT_TRANSLATIONS = {
    'what_type_of_publication_was_the_figure_published_in': 'publication_type_identifier',
    'name_title': 'label',
    'article_title': 'label',
    'book_title': 'label',
    'web_page_title': 'label',
    'conference_title': 'label',
    'title': 'label',
}

PARENT_PUBTYPE_MAP = {
    'report': 'report',
    'journal_article': 'article',
    'book_section': 'report',
    'electronic_article': 'article',
    'web_page': 'webpage',
    'book': 'book',
    'conference_proceedings': 'generic',
}

PARENT_SEARCH_HINTS = {
    'report': {
        'The State of the Climate 2009 Highlights': 'noaa-stateofclim-2009',
        'Global Climate Change Impacts in the United States': 'nca2',
        'Impacts of Climate Change and Variability on Transportation Systems and Infrastructure: Gulf Study, Phase I.': 'ccsp-sap-4_7-2008',
        'Climate and Energy-Water-Land  System Interactions': 'pnnl-21185',
        'Freshwater Use by U.S. Power Plants Electricity\'s thirst for a Precious Resource': 'ucusa-freshwater-2011',
        'New York City Panel on Climate Change Climate Risk Information 2013 Observations, Climate Change Projections and Maps': 'nycpanelonclimch-cri2013',
        'Regional Climate Trends and Scenarios for the U.S. National Climate Assessment. Part 2. Climate of the Southeast U.S.': 'noaa-techreport-nesdis-142-2',
        'Regional Climate Trends and Scenarios for the U.S. National Climate Assessment. Part 3. Climate of the Midwest U.S.': 'noaa-techreport-nesdis-142-3',
        'Reefs at Risk Revisited': ('book', '3788c071-e06a-42c3-b0b9-0396fd494aa3'),
        'Climate Change and Pacific Islands: Indicators and Impacts Report for the 2012 Pacific Islands  Regional Climate Assessment': 'pirca-climate-change-and-pacific-islands',
        'Climate adaptation: Risk, uncertainty and decision-making': 'ukcip-climate-adaptation-risk-uncertainty-and-decision-making',
        'Adapting to Impacts of Climate Change. America\'s Climate Choices: Report of the Panel on 43 Adapting to the Impacts of Climate C': ('book', '1e88532d-c40d-47d2-a872-77b2627fbe89'),
        'Climate Change 2007:  The Physical Science Basis. Contribution of Working Group I to the Fourth Assessment Report of the IPCC': ('book', '92debecd-ca55-46f1-a0c1-734e6b0dc6b1'),
        'Snow, Water, Ice and Permafrost in the Arctic (SWIPA): Climate Change and the Cryosphere': ('book', 'e7c9614c-8db8-410f-9fec-0957292554bf'),
        'Climate Change 2013: The Physical Science Basis. Contribution of Working Group I to the Fifth Assessment  Report of the IPCC': 'ipcc-wg1-ar5-physical-science-basis',
        'Regional Climate Trends and Scenarios for the U.S. National Climate Assessment. Part 9. Climate of the Contiguous United States': 'noaa-techreport-nesdis-142-9',
        'How to Avoid Dangerous Climate Change. A Target for U.S. Emissions Reductions': 'ucusa-howtoavoid-2007',
        'Summary for Decision Makers. Assessment of Climate Change in the Southwest United States': 'swccar-assessment-climate-change-in-southwest-us',
        'Climate Variability and Change in Mobile, Alabama: Task 2 Final Report. Impacts of Climate  25 Change and Variability on Transpo': 'fhwa-hep-12-053',
        'Effects of Climatic Variability and  Change on Forest Ecosystems: A Comprehensive Science  Synthesis for the U.S. Forest  Sector': 'usfs-pnw-gtr-870',
        'Future of America\'s Forests and Rangelands Forest Service. 2010 Resources Planning Act Assessment': 'usfs-gtr-wo-87',
        'Regional Climate Trends and Scenarios for the U.S. National Climate Assessment. Part 5. Climate of the Southwest U.S.': 'noaa-techreport-nesdis-142-5',
        'Regional Climate Trends and Scenarios for the U.S. National Climate Assessment. Part 7. Climate of Alaska': 'noaa-techreport-nesdis-142-7',
        'Reclamation, SECURE Water Act Section 9503(c) - Reclamation Climate Change and Water, Report to  Congress': 'usbr-secure-2011',
        'The Physical Science Basis. Contribution of Working Group I to the Fourth AR4 of IPCC': 'ipcc-wg1-ar5-physical-science-basis',
        '2005 Louisiana Hurricane Impact Atlas': 'lgic-lahurricane-2006',
        '2009 State of the Climate Highlights': 'noaa-stateofclim-2009',
        'Climate of the Southeast United States: Variability, change, impacts and vulnerability.': ('book', '7951fbd8-5877-41aa-ae62-9da3eb56b5c5'),
        'A Reef Manager\'s Guide to Coral Bleaching': ('book', 'd6f69088-1025-4ce7-b0e1-54ab6403a951'),
        'Climate Stabilization Targets: Emissions, Concentrations, and Impacts over Decades to Millennia': ('book', 'f5b281a2-38d2-4633-84db-fd37fa0fb3e6'),
        'Water Resources Sector Technical Input Report in Support of the U.S. Global Change Research Program': 'nca-waterresourcessector-2013',
        'Estimated Use of Water in the United States in 2005': 'usgs-circular-1344',
        'Annual Energy Outlook 2008': 'aeo2008',
        'Value of U.S. agricultural trade, by fiscal year. U.S. Department of Agriculture, Economic Research Service': ('webpage', '319332d5-ec59-4d6d-8411-5eb57f38141d'),
        'Future of America\'s Forest and Rangelands: Forest Service 2010 Resources Planning Act Assessment': 'usfs-gtr-wo-87',
        'Assessment of Climate Change in the Southwest United States: A Report Prepared for the National Climate Assessment': ('book', 'c9625c65-c20f-4163-87fe-cebf734f7836'),
        'Sea-Level Rise for the Coasts of California, Oregon, and Washington: Past, Present, and Future': ('book', 'a36230af-24e6-42c8-8d68-17bcab910595'),
        'Water Planning: A Review of Promising New Methods.': ('generic', '7bd61959-19a0-43ad-80ae-d786619956a1')

    },
    'webpage': {
        'Toxic Algae Bloom in Lake Erie. October 14, 2011': 'afe12af6-a7d3-4b70-99e5-0f80b67b7047',
        'Tribal Energy Program Projects on Tribal Lands': 'abde0ebc-342b-4bb7-b206-016cd3c829c4',
        'Atlas of Rural and Small-Town America. Category: County Classifications. Current Map: Rural-urban Continuum Code, 2013': '2cb79b4a-31cf-43ec-a70a-0371626f1407',
        'Atlas of Rural and Small-Town America. Category: County Classifications. Current Map: Economic Dependence, 1998-2000': '2cb79b4a-31cf-43ec-a70a-0371626f1407',
        'Atlas of Rural and Small-Town America. Category: People.': '2cb79b4a-31cf-43ec-a70a-0371626f1407',
        'St. Petersburg Coastal and Marine Science Center': '2f586ef7-91bb-45e5-b463-ee3e358185ba',
        'NASA Earth Observatory Natural Hazards': 'c57946b1-f413-491f-b75c-1c08f7594f84',
        'Plants of Hawaii': 'a8159919-b01c-442b-afb8-c2e272f81f48',
        'Public Roads': '5f3538ab-eb81-4858-b44e-1304b949b288',
        'Freight Analysis Framework Data Tabulation Tool': '5fe65558-d010-445b-b4f1-9079224dca6b',
        'Ecosystem Services Analysis of Climate Change and Urban Growth in the Upper Santa Cruz Watershed: SCWEPM': 'd4622f7e-aca7-42e6-95da-90579a187c30',
        'State and Local Climate Adaptation': '7de6bfc9-55fa-4d12-ae80-486561b3802c',
        'Climate Change Response Framework - Northwoods': '267378f7-278b-4201-8ffa-a820f5a694b8',
        'NWHI Maps and Publications': 'e6438f11-85f4-4c29-abb5-b09efa3279b2',
        'The Cryosphere Today Compare Daily Sea Ice': 'e4a9eb6a-9421-42c3-94b1-47caf588d41d',
        'NASA Earth Observatory Visualizing the Sea Ice Minimum': '71b4c19e-42da-4f15-99d2-7c7746d8eaf2',
        '2007 Census Ag Atlas Maps: Crops and Plants': 'f39c0146-137f-4668-b401-5972fe40208d',
        'NRCS Photo Gallery': '13da595f-e0f0-4ad0-b87b-44ce3897cd30',
        'Billion-Dollar Weather/Climate Disasters: Mapping': 'd70d7a59-45d7-4b38-baf2-86a7fcf12da3',
        'Before and After: 50 Years of Rising Tides and Sinking Marshes': '6778161f-897b-4f89-942f-8ad2f01f11a0',
        'Influence of El Nino and La Nina on Southwest Rainfall': '6d0a1cba-70fe-4fa3-a630-c45409115ab8',
        'Map of Sea Level Trends': '2ab182cc-171d-4edd-9f9f-51e8b4cc2584',
        'Climate changing our nation\'s landscapes: NOAA, American Public Gardens Association unveil partnership to enhance awareness': 'e4160240-e5ad-41ee-ad56-9cbdaf162369'


    },
    'article': {
        'North American carbon dioxide sources and sinks: magnitude, attribution, and uncertainty': '10.1890/120066',
        'Air Quality and Exercise-Related Health Benefits from Reduced Car Travel  in the Midwestern United States': '10.1289/ehp.1103440',
        'A Shift in Western Tropical Pacific Sea Level Trends during the 1990s': '10.1175/2011JCLI3932.1',
        'An update on Earth\'s energy balance in light of the latest global observations': '10.1038/ngeo1580',
        'About the Lack of Warming...': ('web_page', 'e2ec2d0f-430c-4032-a309-2514ca1f6572'),
        'The Myth of the 1970s Global Cooling Scientific Consensus': '10.1175/2008BAMS2370.1',
        'Hurricane Sandy devestates NY/NJ-area passenger rai systems': ('web_page', '135ae7d9-56e3-4dcb-a81c-42a6f1e9b332'),
        'Climate change impacts of US reactive nitrogen': '10.1073/pnas.1114243109',
        'Range-wide patterns of greater  sage-grouse persistence': '10.1111/j.1472-4642.2008.00502.x',
        'Monitoring and understanding changes in heat waves, cold waves, floods and droughts in the United States: State of Knowledge': '10.1175/BAMS-D-12-00066.1',
        'How do we know the world has warmed?': '10.1175/BAMS-91-7-StateoftheClimate',
        'Attribution of observed historical near-surface temperature variations to anthropogenic and natural causes usingCMIP5simulations': '10.1002/jgrd.50239',
        'Evaluating global trends (1988-2010) in harmonized multi-satellite surface soil moisture': '10.1029/2012gl052988'

    },
    'book': {
        'Climate Change and Pacific Islands: Indicators and Impacts. Report for the 2012 Pacific Islands Regional Climate Assessment': ('report', 'pirca-climate-change-and-pacific-islands'),
        'A focus on climate during the past 100 years in "Climate Variability and Extremes during the Past 100 Years"': '998aa4c2-9f0d-478c-b7bb-19e383c628a9'
    },
    'generic': {
        'Verrazano Narrows Storm Surge Barrier: Against the Deluge: Storm Barriers to  Protect New York City, March 31st 2009': '01d188d1-636b-49e6-af43-c1544cee9319',
        'National Association of Recreation Resource Planners Annual Conference': 'national-association-of-recreation-resource-planners-annual-conference-2005'
    }
}
