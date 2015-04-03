__author__ = 'abuddenberg'

import getpass
import requests
import re

from gcis_clients.domain import Figure, Image, Dataset, Parent


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


def populate_figure(fig_json):
    f = Figure({})
    try:
        f.figure_num, f.title = parse_title(fig_json['graphics_title'])
        f.identifier = fig_json['figure_id'] if fig_json['figure_id'] else re.sub('\W', '_', f.title).lower()
        f.create_dt = fig_json['graphics_create_date']
        f.time_start, f.time_end = fig_json['period_record']
        f.lat_min, f.lat_max, f.lon_min, f.lon_max = fig_json['spatial_extent']
    except Exception, e:
        print e

    return f


def populate_image(img_json):
    img = Image({})
    try:
        img.title = img_json['graphics_title']
        img.identifier = img_json['image_id'] if img_json['image_id'] else re.sub('\W', '_', img.title).lower()
        img.create_dt = img_json['graphics_create_date']
        img.time_start, img.time_end = img_json['period_record']
        img.lat_min, img.lat_max, img.lon_min, img.lon_max = img_json['spatial_extent']
    except Exception, e:
        print e

    return img


def populate_dataset(ds_json):
    ds = Dataset({})
    try:
        ds.name = ds_json['dataset_name']
        ds.url = ds_json['dataset_url']
    except Exception, e:
        print e

    image_select = ds_json['imageSelect'] if 'imageSelect' in ds_json else []
    associated_images = [idx for idx, value in enumerate(image_select) if value == 'on']

    return ds, associated_images


def populate_parent(pub_json):
    p = Parent({})
    try:
        p.publication_type_identifier = pub_json['publicationType'].lower
        p.label = pub_json[''] #title or whatever TODO: add a map for each publication to its title or name
        p.url = ''

    except Exception, e:
        print e

    return p


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
        tier1_json = survey_json[0]['t1']
        fig_json = tier1_json['figure']

        #It's not worth trying to translations on this data; it's too different
        f = populate_figure(fig_json)

        if 'images' in tier1_json:
            images = [populate_image(img) for img in tier1_json['images']]
            f.images.extend(images)

        if 'datasets' in tier1_json:
            datasets = [populate_dataset(ds) for ds in tier1_json['datasets']]

            #Associate datasets with images
            for ds, img_idxs in datasets:
                for idx in img_idxs:
                    f.images[idx].datasets.append(ds)

        if 'origination' in tier1_json and tier1_json['origination'] not in ('Original',):
            f.parents.append(populate_parent(tier1_json['publication']))

        return f

