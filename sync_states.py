__author__ = 'abuddenberg'

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from gcis_clients import GcisClient, SurveyClient, survey_token, gcis_dev_auth, gcis_stage_auth
from gcis_clients.domain import Report, Chapter
from sync_utils import realize_parents, realize_contributors
from states import sync_metadata_tree

import pickle
import sys
import re
import traceback


gcis = GcisClient('https://data-stage.globalchange.gov', *gcis_stage_auth)

surveys = SurveyClient('https://state-resources.cicsnc.org', survey_token)


def main():
    print(gcis.test_login())

    for report_id in sync_metadata_tree:
        for chapter_id in sync_metadata_tree[report_id]:
            for survey_url, figure_id, figure_num in sync_metadata_tree[report_id][chapter_id]:
                figure, datasets = surveys.get_survey(survey_url, do_download=True)

                #Fix misspelling
                figure.identifier = figure_id
                figure.title = figure.title.replace('precipitaton', 'precipitation')
                figure.ordinal = figure_num

                print(survey_url)
                print(figure, datasets)

                realize_parents(gcis, figure.parents)
                realize_contributors(gcis, figure.contributors)

                print('Contributors: ', figure.contributors)
                print('Parents: ', figure.parents)
                # gcis_fig = gcis.get_figure(report_id, figure_id, chapter_id=chapter_id)

                for ds in [p for p in figure.parents if p.publication_type_identifier == 'dataset']:
                    # Assign synthetic activity identifier to for datasets associated with figure
                    if ds.activity and ds.activity.identifier is None:
                        ds.activity.identifier = generate_activity_id(figure, ds.publication)
                    print('Dataset: ', ds.activity)

                print('Creating figure... ', gcis.create_figure(report_id, chapter_id, figure, skip_images=True, skip_upload=False))
                # print('Updating figure... ', gcis.update_figure(report_id, chapter_id, figure, skip_images=True))

    
def generate_activity_id(image, dataset):
    try:
        return '-'.join([image.identifier.split('-')[0], dataset.identifier, 'process'])
    except Exception, e:
        sys.stderr.write('WARNING: Activity identifier generation failed\n')
        traceback.print_exc()


def gen_survey_list():
    # with open('survey_list.pk', 'wb') as out:
    #     pickle.dump(gen_survey_list(), out)
    # surveys = pickle.load(open('survey_list.pk'))
    #
    # for st in sync_metadata_tree['noaa-led-state-summaries-2016']:
    #     print(st)
    #     for f in sorted(surveys[st], key=lambda x: x[1]):
    #         print("('{0}', '{1}', '{2}'),".format(f[0], f[2], f[1]))
    #     print('')

    realized_list = {}

    survey_list = surveys.get_list()
    for i, survey in enumerate(survey_list):
        url = survey['url']
        match = re.match('group/([a-z-]+)', survey['node_title'])
        chapter = match.group(1) if match else ''

        print('Processing: {b}{url} ({i}/{total})'.format(b=surveys.base_url, url=url, i=i + 1, total=len(survey_list)))

        s, ds = surveys.get_survey(url)
        if s:
            print(s.identifier)
            print(chapter, s.ordinal, s.title)

            realized_list.setdefault(chapter, []).append((url, s.ordinal, s.identifier, s.title))
        print('')
    return realized_list


def create_nlss_report():
    nlss = Report({
        'identifier': 'noaa-led-state-summaries-2017',
        'report_type_identifier': 'report',
        'title': 'NOAA-led State Summaries 2017',
        'url': 'https://statesummaries.cicsnc.org/',
        'publication_year': '2017',
        'contact_email': ''
    })

    chapters = [(id, i + 1, ' '.join([w.capitalize() for w in id.split('-')])) for i, id in enumerate(sync_metadata_tree['noaa-led-state-summaries-2017'])]

    print(gcis.create_report(nlss))

    for id, num, title in chapters:
        ch = Chapter({
            'identifier': id,
            'number': num,
            'title': title,
            'report_identifier': nlss.identifier
        })

        print(gcis.create_chapter(nlss.identifier, ch))


main()
