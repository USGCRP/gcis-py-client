__author__ = 'abuddenberg'

import getpass
import requests
import re
from os.path import join, basename

from gcis_clients.domain import Figure, Image, Dataset, Parent, Contributor, Person, Organization
import survey_transforms as trans


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
        f.create_dt = fig_json['graphics_create_date'].strip()
        if any(fig_json['period_record']):
            f.time_start, f.time_end = [d.strip() for d in fig_json['period_record']]
        f.lat_min, f.lat_max, f.lon_min, f.lon_max = fig_json['spatial_extent']
    except Exception, e:
        print 'Figure exception: ', e

    return f


def populate_image(img_json):
    img = Image({})
    try:
        img.title = img_json['graphics_title']
        img.identifier = img_json['image_id'] if 'image_id' in img_json and  img_json['image_id'] else re.sub('\W', '_', img.title).lower()
        img.create_dt = img_json['graphics_create_date'].strip()
        if any(img_json['period_record']):
            img.time_start, img.time_end = [d.strip() for d in img_json['period_record']]
        img.lat_min, img.lat_max, img.lon_min, img.lon_max = img_json['spatial_extent']
    except Exception, e:
        print 'Image exception: ', e

    return img


def populate_dataset(ds_json):
    ds = Dataset({})
    try:
        ds.name = ds_json['dataset_name']
        ds.url = ds_json['dataset_url']
    except Exception, e:
        print 'Dataset exception: ', e

    image_select = ds_json['imageSelect'] if 'imageSelect' in ds_json else []
    associated_images = [idx for idx, value in enumerate(image_select) if value == 'on']

    return ds, associated_images


def populate_parent(pub_json):
    p = Parent({})
    try:
        p = Parent(pub_json, trans=trans.PARENT_TRANSLATIONS, pubtype_map=trans.PARENT_PUBTYPE_MAP)
        p.url = ''

    except Exception, e:
        print 'Parent exception: ', e

    return p


def populate_contributors(field):
    s = field.split(',')
    name, rest = s[0], s[1:]

    name_split = name.split()
    first_name, last_name = name_split[0], name_split[-1]
    org_name = rest[0] if len(rest) > 0 else None

    contributor = Contributor({}, hints=trans.CONTRIB_ROLES)
    contributor.person = Person({'first_name': first_name, 'last_name': last_name})
    contributor.organization = Organization({'name': org_name}, known_ids=trans.ORG_IDS)

    return contributor


class SurveyClient:
    def __init__(self, url, token, local_download_dir=None):
        self.base_url = url

        #If token was not provided, obtain it
        if token is None:
            token = get_credentials()

        self.token = token

        if local_download_dir:
            self.local_download_dir = local_download_dir
        else:
            from gcis_clients import default_image_dir
            self.local_download_dir = default_image_dir()

    def get_list(self):
        url = '{b}/metadata/list?token={t}'.format(b=self.base_url, t=self.token)
        print url
        return requests.get(url).json()

    def get_survey(self, fig_url, do_download=False):
        full_url = '{b}{url}?token={t}'.format(b=self.base_url, url=fig_url, t=self.token)
        survey_json = requests.get(full_url).json()
        tier1_json = survey_json[0]['t1'] if len(survey_json) > 0 and survey_json[0]['t1'] is not None else []

        f = None

        if 'figure' in tier1_json:
            figure_json = tier1_json['figure']
            #It's not worth trying to translations on this data; it's too different
            f = populate_figure(figure_json)
            f.remote_path = survey_json[0]['filepath']
            f.local_path = join(self.local_download_dir, basename(f.remote_path)) if f.remote_path else None

            if 'origination' in figure_json and figure_json['origination'] not in ('Original',) and 'publication' in figure_json:
                f.parents.append(populate_parent(figure_json['publication']))

        if 'images' in tier1_json:
            images = [populate_image(img) for img in tier1_json['images']]
            f.images.extend(images)
        elif 'figure' in tier1_json:
            default_image = populate_image(tier1_json['figure'])
            f.images.append(default_image)

        if 'datasets' in tier1_json:
            datasets = [populate_dataset(ds) for ds in tier1_json['datasets']]

            #Associate datasets with images
            for ds, img_idxs in datasets:
                for idx in img_idxs:
                    try:
                        f.images[idx].datasets.append(ds)
                    except Exception, e:
                        print 'Association exception: ', e

        if 'poc' in tier1_json:
            f.add_contributor(populate_contributors(tier1_json['poc']))

        if do_download:
            self.download_figure(f)

        return f

    def download_figure(self, figure):
        url = '{b}/{path}?token={t}'.format(b=self.base_url, path=figure.remote_path, t=self.token)
        resp = requests.get(url, stream=True)

        if resp.status_code == 200:
            filepath = join(self.local_download_dir, figure.remote_path.split('/')[-1])
            with open(filepath, 'wb') as fig_out:
                for bytes in resp.iter_content(chunk_size=4096):
                    fig_out.write(bytes)

            return filepath
        elif resp.status_code == 404:
            raise Exception('Image not found: {u}'.format(u=url))
        else:
            raise Exception(resp.status_code)