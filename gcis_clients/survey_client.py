__author__ = 'abuddenberg'

import getpass
import requests
import re

from gcis_clients.domain import Figure


def get_credentials():
    #First check our magic enviroment variable (SURVEY_TOKEN)
    from gcis_clients import webform_token

    if webform_token is not None:
        return webform_token

    else:
        return getpass.getpass('Survey token: ')


def parse_title(graphic_title):
    match = re.search('\d+\.\d+', graphic_title)
    if match:
        return match.group(0), graphic_title[match.end(0):].strip()
    else:
        return None, graphic_title


class SurveyClient:
    def __init__(self, url, token, local_image_dir=None, remote_dir='/system/files/'):
        self.base_url = url

        #If token was not provided, obtain it
        if token is None:
            token = get_credentials()

        self.token = token

        if local_image_dir:
            self.images_dir = local_image_dir
        else:
            from gcis_clients import default_image_dir
            self.images_dir = default_image_dir()
        self.remote_image_dir = remote_dir

    def get_list(self):
        url = '{b}/metadata/list?token={t}'.format(b=self.base_url, t=self.token)
        return requests.get(url).json()

    def get_survey(self, fig_url, download_images=False):
        full_url = '{b}{url}?token={t}'.format(b=self.base_url, url=fig_url, t=self.token)
        survey_json = requests.get(full_url).json()
        fig_json = survey_json[0]['t1']['figure']

        #It's not worth trying to translations on this data; it's too different
        f = Figure({})
        f.figure_num, f.title = parse_title(fig_json['graphics_title'])
        f.identifier = fig_json['figure_id'] if fig_json['figure_id'] else re.sub('\W', '_', f.title).lower()
        f.time_start, f.time_end = fig_json['period_record']
        f.lat_min, f.lat_max, f.lon_min, f.lon_max = fig_json['spatial_extent']
        f.create_dt = fig_json['graphics_create_date']

        __blah = [
            'keywords',
            'report_identifier', 'chapter', 'submission_dt',
            'source_citation', 'attributes', 'chapter_identifier', 'images'
        ]

        return f

