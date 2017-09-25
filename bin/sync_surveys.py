__author__ = 'abuddenberg'

from gcis_clients import GcisClient, SurveyClient, survey_token, gcis_dev_auth, gcis_stage_auth
from gcis_clients.domain import Report, Chapter
# from sync_utils import realize_parents, realize_contributors

from collections import OrderedDict

import pickle
import sys

# gcis = GcisClient('http://data.gcis-dev-front.joss.ucar.edu', *gcis_dev_auth)
gcis = GcisClient('https://data-stage.globalchange.gov', *gcis_stage_auth)

surveys = SurveyClient('https://healthresources.cicsnc.org', survey_token)

sync_metadata_tree = {
    'usgcrp-climate-human-health-assessment-2016': OrderedDict([
        ('front-matter', [
            ('/metadata/figures/3931', 'understanding-the-exposure-pathway-diagrams'),
        ]),
        ('executive-summary', [
            ('/metadata/figures/3906', 'examples-of-climate-impacts-on-human-health'),
            ('/metadata/figures/3832', 'es-climate-change-and-health'),
            ('/metadata/figures/3833', 'es-projected-changes-in-deaths-in-us-cities-by-season'),
            ('/metadata/figures/3834', 'es-projected-change-in-temperature-ozone-and-ozone-related-premature-deaths-in-2030'),
            ('/metadata/figures/3838', 'es-estimated-deaths-and-billion-dollar-losses-from-extreme-weather-events-in-the-u-s-2004-2013'),
            ('/metadata/figures/3835', 'es-changes-in-lyme-disease-case-report-distribution'),
            ('/metadata/figures/3836', 'es-links-between-climate-change-water-quantity-and-quality-and-human-exposure-to-water-related-illness'),
            ('/metadata/figures/3837', 'es-farm-to-table'),
            ('/metadata/figures/3839', 'es-the-impact-of-climate-change-on-physical-mental-and-community-health'),
            ('/metadata/figures/3840', 'es-determinants-of-vulnerability')
        ]),
        ('climate-change-and-human-health', [
            ('/metadata/figures/3698', 'major-us-climate-trends'), #1.1 #climate-change-and-human-health
            ('/metadata/figures/3632', 'change-in-number-of-extreme-precipitation-events'), #1.2 #climate-change-and-human-health
            ('/metadata/figures/3635', 'projected-changes-in-temperature-and-precipitation-by-mid-century'), #1.3 #climate-change-and-human-health
            ('/metadata/figures/3633', 'projected-changes-in-hottest-coldest-and-wettest-driest-day-of-the-year'), #1.4 #climate-change-and-human-health
            ('/metadata/figures/3757', 'climate-change-and-health'), #1.5 #climate-change-and-human-health
            ('/metadata/figures/3933', 'sources-of-uncertainty'), #1.6 #climate-change-and-human-health
        ]),
        ('temperature-related-death-and-illness', [
            ('/metadata/figures/3811', 'climate-change-and-health-extreme-heat'), #2.1 #temperature-related-death-and-illness
            ('/metadata/figures/3585', 'heat-related-deaths-during-the-1995-chicago-heat-wave'), #2.2 #temperature-related-death-and-illness
            ('/metadata/figures/3643', 'projected-changes-in-temperature-related-death-rates'), #2.3 #temperature-related-death-and-illness
            ('/metadata/figures/3653', 'projected-changes-in-deaths-in-us-cities-by-season'), #2.4 #temperature-related-death-and-illness
        ]),
        ('air-quality-impacts', [
            ('/metadata/figures/3812', 'climate-change-and-health-outdoor-air-quality'), #3.1 #air-quality-impacts
            ('/metadata/figures/3647', 'projected-change-in-temperature-ozone-and-ozone-related-premature-deaths-in-2030'), #3.2 #air-quality-impacts
            ('/metadata/figures/3649', 'projected-change-in-ozone-related-premature-deaths'), #3.3 #air-quality-impacts
            ('/metadata/figures/3650', 'ragweed-pollen-season-lengthens'), #3.4 #air-quality-impacts
        ]),
        ('extreme-events', [
            ('/metadata/figures/3810', 'estimated-deaths-and-billion-dollar-losses-from-extreme-weather-events-in-the-us-2004-2013'), #4.1 #extreme-weather #Has Activities
            ('/metadata/figures/3808', 'climate-change-and-health-flooding'), #4.2 #extreme-weather
            ('/metadata/figures/3760', 'hurricane-induced-flood-effects-in-eastern-and-central-united-states'), #4.3 #extreme-weather
            ('/metadata/figures/3907', 'projected-increases-in-very-large-fires'), #4.4 #extreme-weather
        ]),
        ('vectorborne-diseases', [
            ('/metadata/figures/3807', 'climate-change-and-health-lyme-disease'), #5.1 #vectorborne-diseases
            ('/metadata/figures/3659', 'changes-in-lyme-disease-case-report-distribution'), #5.2 #vectorborne-diseases
            ('/metadata/figures/3658', 'life-cycle-of-blacklegged-ticks-ixodes-scapularis'), #5.3 #vectorborne-diseases
            ('/metadata/figures/3747', 'projected-change-in-lyme-disease-onset-week'), #5.4 #vectorborne-diseases
            ('/metadata/figures/3674', 'incidence-of-west-nile-neuroinvasive-disease-by-county-in-the-united-states'), #5.5 #vectorborne-diseases
            ('/metadata/figures/3675', 'climate-impacts-on-west-nile-virus-transmission'), #5.6 #vectorborne-diseases
        ]),
        ('water-related-illnesses', [
            ('/metadata/figures/3824', 'climate-change-and-health-vibrio'), #5.1 #water-related-illnesses
            ('/metadata/figures/3700', 'links-between-climate-change-water-quantity-and-quality-and-human-exposure-to-water-related-illness'), #5.2 #water-related-illnesses  #TOO BIG
            ('/metadata/figures/3671', 'locations-of-livestock-and-projections-of-heavy-precipitation'), #5.3 #water-related-illnesses #TOO BIG
            ('/metadata/figures/3709', 'projections-of-vibrio-occurrence-and-abundance-in-chesapeake-bay'), #5.4 #water-related-illnesses
            ('/metadata/figures/3704', 'changes-in-suitable-coastal-vibrio-habitat-in-alaska'), #5.5 #water-related-illnesses
            ('/metadata/figures/3734', 'projected-changes-in-caribbean-gambierdiscus-species'), #5.6 #water-related-illnesses
            ('/metadata/figures/3712', 'projections-of-growth-of-alexandrium-in-puget-sound'), #5.7 #water-related-illnesses
        ]),
        ('food-safety-nutrition-and-distribution', [
            ('/metadata/figures/3579', 'farm-to-table'), #7.1 #food-safety-nutrition-and-distribution
            # ('/metadata/figures/3600', 'mycotoxin-in-corn'), #7.1 #food-safety-nutrition-and-distribution BOX 1?
            ('/metadata/figures/3809', 'climate-change-and-health-salmonella'), #7.2 #food-safety-nutrition-and-distribution
            ('/metadata/figures/3748', 'seasonality-of-human-illnesses-associated-with-foodborne-pathogens'), #7.3 #food-safety-nutrition-and-distribution
            ('/metadata/figures/3688', 'effects-of-carbon-dioxide-on-protein-and-minerals'), #7.4 #food-safety-nutrition-and-distribution
            ('/metadata/figures/3597', 'mississippi-river-level-at-st-louis-missouri'), #7.5 #food-safety-nutrition-and-distribution
            # ('/metadata/figures/3600', 'mycotoxin-in-corn'), #Box 7,1
            # ('/metadata/figures/3806', 'low-water-conditions-on-mississippi-river')
        ]),
        ('mental-health-and-well-being', [
            ('/metadata/figures/3789', 'climate-change-and-mental-health'), #8.1 #mental-health-and-well-being
            ('/metadata/figures/3722', 'the-impact-of-climate-change-on-physical-mental-and-community-health'), #8.2 #mental-health-and-well-being
        ]),
        ('populations-of-concern', [
            ('/metadata/figures/3696', 'determinants-of-vulnerability'), #9.1 #populations-of-concern
            ('/metadata/figures/3917', 'intersection-of-social-determinants-of-health-and-vulnerability'), #9.2 #populations-of-concern
            ('/metadata/figures/3758', 'vulnerability-to-the-health-impacts-of-climate-change-at-different-lifestages'), #9.3 #populations-of-concern
            ('/metadata/figures/3714', 'mapping-social-vulnerability'), #9.4 #populations-of-concern
            ('/metadata/figures/3717', 'mapping-communities-vulnerable-to-heat-in-georgia'), #9.5 #populations-of-concern
        ]),
        ('appendix-1--technical-support-document', [
            ('/metadata/figures/3623', 'scenarios-of-future-temperature-rise'), #1.1 #climate-change-and-human-health
            ('/metadata/figures/3939', 'example-increasing-spatial-resolution-of-climate-models'), #1.2 #climate-change-and-human-health
            ('/metadata/figures/3638', 'sensitivity-analysis-of-differences-in-modeling-approaches'), #1.3 #climate-change-and-human-health
            ('/metadata/figures/3932', 'tsd-sources-of-uncertainty'), #1.4 #climate-change-and-human-health
        ])
    ])
}

def main():
    print gcis.test_login()
    image_id_map = pickle.load(open('image_id_cache.pk1', 'r'))
    # regenerate_image_id_map(existing=image_id_map)
    # create_health_report()
    # create_cmip5_report()

    for report_id in sync_metadata_tree:
        for chapter_id in sync_metadata_tree[report_id]:
            for survey_url, figure_id in sync_metadata_tree[report_id][chapter_id]:
                figure, datasets = surveys.get_survey(survey_url, do_download=False)

                resp = gcis.post_figure_original(report_id, figure_id, figure.original, chapter_id=chapter_id)
                print(resp.status_code, resp.text)
                # gcis_fig = gcis.get_figure(report_id, figure_id, chapter_id=chapter_id)
                #
                # print survey_url, gen_edit_link(survey_url)
                #
                # figure, datasets = surveys.get_survey(survey_url, do_download=False)
                #
                # #Override identifier
                # figure.identifier = figure_id
                #
                # #Pull existing captions
                # if gcis.figure_exists(report_id, figure_id, chapter_id=chapter_id):
                #     gcis_fig = gcis.get_figure(report_id, figure_id, chapter_id=chapter_id)
                #     figure.caption = gcis_fig.caption
                #     figure.files = gcis_fig.files
                #
                # realize_parents(gcis, figure.parents)
                # realize_contributors(gcis, figure.contributors)
                #
                # print 'Contributors: ', figure.contributors
                # print 'Parents: ', figure.parents
                #
                # for ds in [p for p in figure.parents if p.publication_type_identifier == 'dataset']:
                #     # Assign synthetic activity identifier to for datasets associated with figure
                #     if ds.activity and ds.activity.identifier is None:
                #         ds.activity.identifier = generate_activity_id(figure, ds.publication)
                #     print 'Dataset: ', ds.activity
                #
                # #Create the figure in GCIS
                # # print 'Creating figure... ', gcis.create_figure(report_id, chapter_id, figure, skip_images=True, skip_upload=False)
                # print 'Updating figure... ', gcis.update_figure(report_id, chapter_id, figure, skip_images=True)
                # # print 'Deleting old file', gcis.delete_file(figure.files[0])
                # # print 'Uploading...', gcis.upload_figure_file(report_id, chapter_id, figure_id, figure.local_path)
                #
                # for i in figure.images:
                #     i.identifier = image_id_map[(figure_id, i.identifier)]
                #     print '\t', i
                #
                #     realize_parents(gcis, i.parents)
                #     realize_contributors(gcis, i.contributors)
                #
                #     print '\t\tContributors: ', i.contributors
                #     print '\t\tParents: ', i.parents
                #     for ds in [p for p in i.parents if p.publication_type_identifier == 'dataset']:
                #         # Assign synthetic activity identifier to for datasets associated with images
                #         if ds.activity and ds.activity.identifier is None:
                #             ds.activity.identifier = generate_activity_id(i, ds.publication)
                #         print '\t\tDataset: ', ds, ds.activity
                #
                #     #Create image in GCIS
                #     # print 'Creating image... ', gcis.create_image(i, report_id=report_id, figure_id=figure_id)
                #     print 'Updating image... ', gcis.update_image(i)



def gen_edit_link(survey_id):
    node_id = survey_id.split('/')[-1]
    return 'https://healthresources.globalchange.gov/node/' + node_id


def generate_activity_id(image, dataset):
    try:
        return '-'.join([image.identifier.split('-')[0], dataset.identifier, '-process'])
    except Exception, e:
        sys.stderr.write('WARNING: Activity identifier generation failed\n')


def regenerate_image_id_map(existing=None):
    from uuid import uuid4
    image_id_map = existing if existing else {}

    for report_id in sync_metadata_tree:
        for chapter_id in sync_metadata_tree[report_id]:
            for survey_url, figure_id in sync_metadata_tree[report_id][chapter_id]:
                s, ds = surveys.get_survey(survey_url, do_download=False)
                for img in s.images:
                    if (figure_id, img.identifier) in image_id_map:
                        print 'skipping: ', (figure_id, img.identifier)
                        continue
                    else:
                        print 'added: ', (figure_id, img.identifier)
                        image_id_map[(figure_id, img.identifier)] = str(uuid4())

    with open('image_id_cache.pk1', 'wb') as fout:
        pickle.dump(image_id_map, fout)
    print 'image_id_map regenerated'


def gen_survey_list():
    realized_list = []
    chapters = [c for c in sync_metadata_tree['usgcrp-climate-human-health-assessment-2016']]

    survey_list = surveys.get_list()
    for i, survey in enumerate(survey_list):
        url = survey['url']
        print 'Processing: {b}{url} ({i}/{total})'.format(b=surveys.base_url, url=url, i=i + 1, total=len(survey_list))

        s = surveys.get_survey(url)
        chp_id = chapters[s.chapter] if s and s.chapter else None
        if s:
            print s.identifier
            print chp_id, s.figure_num, s.title

            realized_list.append((chp_id, s.figure_num, s.identifier, s.title, url))
        print ''
    return realized_list


def create_health_report():
    hr = Report({
        'identifier': 'usgcrp-climate-human-health-assessment-2016',
        'report_type_identifier': 'assessment',
        'title': 'The Impacts of Climate Change on Human Health in the United States: A Scientific Assessment',
        'url': 'http://www.globalchange.gov/health-assessment',
        'publication_year': '2016',
        'contact_email': 'healthreport@usgcrp.gov'
    })

    # ['report_identifier', 'identifier', 'number', 'title', 'url']
    chapters = [
        ('executive-summary', None, 'Executive Summary'),
        ('climate-change-and-human-health', 1, 'Climate Change and Human Health'),
        ('temperature-related-death-and-illness', 2, 'Temperature-Related Death and Illness'),
        ('air-quality-impacts', 3, 'Air Quality Impacts'),
        ('extreme-events', 4, 'Impacts of Extreme Events on Human Health'),
        ('vectorborne-diseases', 5, 'Vectorborne Diseases'),
        ('water-related-illnesses', 6, 'Climate Impacts on Water-Related Illnesses'),
        ('food-safety--nutrition--and-distribution', 7, 'Food Safety, Nutrition, and Distribution'),
        ('mental-health-and-well-being', 8, 'Mental Health and Well-Being'),
        ('populations-of-concern', 9, 'Climate-Health Risk Factors and Populations of Concern'),
        ('appendix-1--technical-support-document', None, 'Appendix 1: Technical Support Document'),
        ('appendix-2--process-for-literature-review', None, 'Appendix 2: Process for Literature Review'),
        ('appendix-3--report-requirements-development-process-review-and-approval', None, 'Appendix 3: Report Requirements, Development Process, Review, and Approval'),
        ('appendix-4--documenting-uncertainty-confidence-and-likelihood', None, 'Appendix 4: Documenting Uncertainty: Confidence and Likelihood'),
        ('appendix-5--glossary-and-acronyms', None, 'Appendix 5: Glossary and Acronyms'),
        ('front-matter', None, 'Front Matter')
    ]

    print gcis.create_report(hr)

    for id, num, title in chapters:
        ch = Chapter({
            'identifier': id,
            'number': num,
            'title': title,
            'report_identifier': hr.identifier
        })

        print gcis.create_chapter(hr.identifier, ch)


def create_cmip5_report():
    cmip = Report({
        'identifier': 'noaa-techreport-nesdis-144',
        'report_type_identifier': 'report',
        'title': 'Regional Surface Climate Conditions in CMIP3 and CMIP5 for the United States: Differences, Similarities, and Implications for the U.S. National Climate Assessment',
        'publication_year': '2015'
    })

    print gcis.create_report(cmip)

    chapters = [
        ('introduction', 1, 'Introduction'),
        ('data', 2, 'Data'),
        ('methods', 3, 'Methods'),
        ('temperature', 4, 'Temperature'),
        ('precipitation', 5, 'Precipitation'),
        ('summary', 6, 'Summary'),
        ('appendix', None, 'Appendix'),
        ('references', None, 'References'),
        ('acknowledgements', None, 'Acknowledgements'),
    ]

    for id, num, title in chapters:
        ch = Chapter({
            'identifier': id,
            'number': num,
            'title': title,
            'report_identifier': cmip.identifier
        })

        print gcis.create_chapter(cmip.identifier, ch)

main()
