import json
import os
from os.path import basename, expanduser
import re
import requests
import yaml
import getpass

from domain import Figure, Image, Dataset, Activity, Person, Organization, Article, Webpage, Report


def check_image(fn):
    def wrapped(*args, **kwargs):
        # if len(args) < 1 or not isinstance(args[0], Image):
        #     raise Exception('Invalid Image')
        if args[1].identifier in (None, ''):
            raise Exception('Invalid identifier', args[1].identifier)
        return fn(*args, **kwargs)

    return wrapped


def exists(fn):
    def wrapped(*args, **kwargs):
        resp = fn(*args, **kwargs)
        if resp.status_code == 200:
            return True
        elif resp.status_code == 404:
            return False
        else:
            raise Exception(resp.text)
    return wrapped


def http_resp(fn):
    def wrapped(*args, **kwargs):
        resp = fn(*args, **kwargs)
        if resp.status_code == 200:
            return resp
        else:
            raise Exception('{url}\n{stat} {txt}'.format(url=resp.url, stat=resp.status_code, txt=resp.text))
    return wrapped


def get_credentials(url):
    #First check our magic enviroment variables (GCIS_USER and GCIS_KEY)
    from gcis_clients import gcis_auth
    env_user, env_key = gcis_auth

    if env_user is not None and env_key is not None:
        return env_user, env_key

    #Next, see if we can find Gcis.conf somewhere
    conf_possibilities = [expanduser(f) for f in ['~/etc/Gcis.conf', '~/.gcis-py-client/Gcis.conf'] if
                          os.path.exists(expanduser(f))]

    for gcis_config in conf_possibilities:
        print 'Using {gc} for credentials...'.format(gc=gcis_config)
        all_creds = yaml.load(open(gcis_config, 'r'))
        instance_creds = [c for c in all_creds if c['url'] == url][0]

        return instance_creds['userinfo'].split(':')

    #Else prompt for credentials
    #Wow, I managed to use it
    else:
        username = raw_input('Username: ')
        api_key = getpass.getpass('API key: ')

        return username, api_key


class AssociationException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GcisClient(object):
    def __init__(self, *args, **kwargs):
        username = None
        api_key = None
        
        #Handle varargs
        #User only specifies url
        if len(args) == 1:
            self.base_url = args[0]
        #User provides url, username, and key
        elif len(args) == 3:
            self.base_url = args[0]
            username, api_key = args[1:3]
        #User provides none or inconsistent args
        else:
            self.base_url = 'http://data.globalchange.gov'

        #If credentials were not provided, obtain them 
        if username is None or api_key is None:
            username, api_key = get_credentials(self.base_url)

        #Squash trailing slash in base_url, if given
        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]

        self.s = requests.Session()
        self.s.auth = (username, api_key)
        self.s.headers.update({'Accept': 'application/json'})

    @http_resp
    def create_figure(self, report_id, chapter_id, figure, skip_images=False):
        if figure.identifier in (None, ''):
            raise Exception('Invalid figure identifier', figure.identifier)

        #Is GCIS not inferring this from the url parameter?
        if figure.chapter_identifier in (None, ''):
            figure.chapter_identifier = chapter_id

        url = '{b}/report/{rpt}/chapter/{chp}/figure/'.format(
            b=self.base_url, rpt=report_id, chp=chapter_id
        )

        resp = self.s.post(url, data=figure.as_json(), verify=False)
        if resp.status_code != 200:
            return resp

        if figure.local_path is not None:
            self.upload_figure_file(report_id, chapter_id, figure.identifier, figure.local_path)

        if skip_images is False:
            for image in figure.images:
                self.create_image(image),
                self.associate_image_with_figure(image.identifier, report_id, figure.identifier)

        for c in figure.contributors:
            self.associate_contributor_with_figure(c, report_id, chapter_id, figure.identifier)

        for p in figure.parents:
            if p.activity:
                self.create_or_update_activity(p.activity)
            activity_id = p.activity.identifier if p.activity else None
            self.associate_figure_with_parent(report_id, figure.identifier, p, activity_id=activity_id)

        return resp

    @http_resp
    def update_figure(self, report_id, chapter_id, figure, skip_images=False, old_id=None):
        if figure.identifier in (None, ''):
            raise Exception('Invalid identifier', figure.identifier)

        #Is GCIS not inferring this from the url parameter?
        if figure.chapter_identifier in (None, ''):
            figure.chapter_identifier = chapter_id

        url = '{b}/report/{rpt}/chapter/{chp}/figure/{fig}'.format(
            b=self.base_url, rpt=report_id, chp=chapter_id, fig=old_id or figure.identifier
        )

        resp = self.s.post(url, data=figure.as_json(), verify=False)

        if skip_images is False:
            for image in figure.images:
                self.update_image(image)

        for c in figure.contributors:
            self.associate_contributor_with_figure(c, report_id, chapter_id, figure.identifier)

        for p in figure.parents:
            if p.activity:
                self.create_or_update_activity(p.activity)
            activity_id = p.activity.identifier if p.activity else None
            self.associate_figure_with_parent(report_id, figure.identifier, p, activity_id=activity_id)

        return resp

    @http_resp
    def delete_figure(self, report_id, figure_id):
        url = '{b}/report/{rpt}/figure/{fig}'.format(b=self.base_url, rpt=report_id, fig=figure_id)
        return self.s.delete(url, verify=False)

    @http_resp
    def upload_figure_file(self, report_id, chapter_id, figure_id, local_path):
        url = '{b}/report/{rpt}/chapter/{chp}/figure/files/{id}/{fn}'.format(b=self.base_url, rpt=report_id, chp=chapter_id, id=figure_id, fn=basename(local_path))
        # For future multi-part encoding support
        # return self.s.put(url, headers=headers, files={'file': (filename, open(filepath, 'rb'))})
        if not os.path.exists(local_path):
            raise Exception('File not found: ' + local_path)

        return self.s.put(url, data=open(local_path, 'rb'), verify=False)

    @check_image
    def create_image(self, image, report_id=None, figure_id=None):
        url = '{b}/image/'.format(b=self.base_url)
        resp = self.s.post(url, data=image.as_json(), verify=False)

        if resp.status_code != 200:
            return resp
        
        if image.local_path is not None:
            self.upload_image_file(image.identifier, image.local_path)
        if figure_id and report_id:
            self.associate_image_with_figure(image.identifier, report_id, figure_id)
        # for dataset in image.datasets:
        #     if not self.dataset_exists(dataset.identifier):
        #         self.create_dataset(dataset)
        #     # if not self.activity_exists(dataset.activity.identifier):
        #     #     self.create_activity(dataset.activity))
        #     self.create_or_update_activity(dataset.activity)
        #     self.associate_image_with_parent(dataset.identifier, image.identifier,
        #                                       activity_id=dataset.activity.identifier)
        for p in image.parents:
            if p.activity:
                self.create_or_update_activity(p.activity)

            activity_id = p.activity.identifier if p.activity else None
            self.associate_image_with_parent(image.identifier, p, activity_id=activity_id)
        return resp

    @check_image
    def update_image(self, image, old_id=None):
        url = '{b}/image/{img}'.format(b=self.base_url, img=old_id or image.identifier)
        for c in image.contributors:
            self.associate_contributor_with_image(c, image.identifier)

        for p in image.parents:
            if p.activity:
                self.create_or_update_activity(p.activity)
            activity_id = p.activity.identifier if p.activity else None
            self.associate_image_with_parent(image.identifier, p, activity_id=activity_id)

        return self.s.post(url, data=image.as_json(), verify=False)

    @check_image
    @http_resp
    def delete_image(self, image):
        delete_url = '{b}/image/{img}'.format(b=self.base_url, img=image.identifier)
        return self.s.delete(delete_url, verify=False)

    @http_resp
    def associate_image_with_figure(self, image_id, report_id, figure_id):
        url = '{b}/report/{rpt}/figure/rel/{fig}'.format(b=self.base_url, rpt=report_id, fig=figure_id)
        return self.s.post(url, data=json.dumps({'add_image_identifier': image_id}), verify=False)

    @http_resp
    def upload_image_file(self, image_id, local_path):
        url = '{b}/image/files/{id}/{fn}'.format(b=self.base_url, id=image_id, fn=basename(local_path))
        # For future multi-part encoding support
        # return self.s.put(url, headers=headers, files={'file': (filename, open(filepath, 'rb'))})
        if not os.path.exists(local_path):
            raise Exception('File not found: ' + local_path)

        return self.s.put(url, data=open(local_path, 'rb'), verify=False)

    #Full listing
    def get_figure_listing(self, report_id, chapter_id=None):
        chapter_filter = '/chapter/' + chapter_id if chapter_id else ''

        url = '{b}/report/{rpt}{chap}/figure'.format(b=self.base_url, rpt=report_id, chap=chapter_filter)
        resp = self.s.get(url, params={'all': '1'}, verify=False)

        try:
            return [Figure(figure) for figure in resp.json()]
        except ValueError:
            raise Exception(resp.text)

    def get_figure(self, report_id, figure_id, chapter_id=None):
        chapter_filter = '/chapter/' + chapter_id if chapter_id else ''

        url = '{b}/report/{rpt}{chap}/figure/{fig}'.format(
            b=self.base_url, rpt=report_id, chap=chapter_filter, fig=figure_id
        )
        resp = self.s.get(url, params={'all': '1'}, verify=False)

        try:
            return Figure(resp.json())
        except ValueError:
            raise Exception(resp.text)

    @exists
    def figure_exists(self, report_id, figure_id, chapter_id=None):
        chapter_filter = '/chapter/' + chapter_id if chapter_id else ''

        url = '{b}/report/{rpt}{chap}/figure/{fig}'.format(
            b=self.base_url, rpt=report_id, chap=chapter_filter, fig=figure_id
        )
        return self.s.head(url, verify=False)

    def get_image(self, image_id):
        url = '{b}/image/{img}'.format(b=self.base_url, img=image_id)
        resp = self.s.get(url, verify=False)

        try:
            return Image(resp.json())
        except ValueError:
            raise Exception(resp.text)

    @exists
    def image_exists(self, image_id):
        url = '{b}/image/{img}'.format(b=self.base_url, img=image_id)
        return self.s.head(url, verify=False)

    def has_all_associated_images(self, report_id, figure_id, target_image_ids):
        try:
            figure_image_ids = [i.identifier for i in self.get_figure(report_id, figure_id).images]
        except Exception, e:
            print e.message
            return False, set()

        target_set = set(target_image_ids)
        gcis_set = set(figure_image_ids)
        deltas = target_set - gcis_set

        if target_set.issubset(gcis_set):
            return True, deltas
        else:
            return False, deltas

    def test_login(self):
        url = '{b}/login.json'.format(b=self.base_url)
        resp = self.s.get(url, verify=False)
        return resp.status_code, resp.text

    def get_report(self, report_id):
        url = '{b}/report/{id}'.format(b=self.base_url, id=report_id)
        resp = self.s.get(url, verify=False)

        try:
            return Report(resp.json())
        except ValueError:
            raise Exception(resp.text)

    @exists
    def report_exists(self, report_id):
        url = '{b}/report/{id}'.format(b=self.base_url, id=report_id)
        return self.s.head(url, verify=False)

    @http_resp
    def create_report(self, report):
        url = '{b}/report/'.format(b=self.base_url)
        return self.s.post(url, data=report.as_json(), verify=False)

    @http_resp
    def update_report(self, report, old_id=None):
        url = '{b}/report/{id}'.format(b=self.base_url, id=old_id or report.identifier)
        return self.s.post(url, data=report.as_json(), verify=False)

    @http_resp
    def delete_report(self, report):
        url = '{b}/report/{ds}'.format(b=self.base_url, ds=report.identifier)
        return self.s.delete(url, verify=False)

    @http_resp
    def get_chapter(self, chapter_id):
        url = '{b}/chapter/{id}'.format(b=self.base_url, id=chapter_id)
        resp = self.s.get(url, verify=False)

        return resp.json()

    @exists
    def chapter_exists(self, report_id, chapter_id):
        url = '{b}/report/{rpt}/chapter/{id}'.format(b=self.base_url, rpt=report_id, id=chapter_id)
        return self.s.head(url, verify=False)

    @http_resp
    def create_chapter(self, report_id, chapter):
        url = '{b}/report/{rpt}/chapter/'.format(b=self.base_url, rpt=report_id)
        return self.s.post(url, data=chapter.as_json(), verify=False)

    @http_resp
    def update_chapter(self, chapter, old_id=None):
        url = '{b}/chapter/{id}'.format(b=self.base_url, id=old_id or chapter.identifier)
        return self.s.post(url, data=chapter.as_json(), verify=False)

    @http_resp
    def delete_chapter(self, chapter):
        url = '{b}/chapter/{ds}'.format(b=self.base_url, ds=chapter.identifier)
        return self.s.delete(url, verify=False)

    def get_keyword_listing(self):
        url = '{b}/gcmd_keyword'.format(b=self.base_url)
        resp = self.s.get(url, params={'all': '1'}, verify=False)

        return resp.json()

    def get_keyword(self, key_id):
        url = '{b}/gcmd_keyword/{k}'.format(b=self.base_url, k=key_id)
        return self.s.get(url, verify=False).json()

    def associate_keyword_with_figure(self, keyword_id, report_id, figure_id):
        url = '{b}/report/{rpt}/figure/keywords/{fig}'.format(b=self.base_url, rpt=report_id, fig=figure_id)
        return self.s.post(url, data=json.dumps({'identifier': keyword_id}), verify=False)

    def get_dataset(self, dataset_id):
        url = '{b}/dataset/{ds}'.format(b=self.base_url, ds=dataset_id)
        resp = self.s.get(url, verify=False)
        try:
            return Dataset(resp.json())
        except ValueError:
            raise Exception(resp.text)

    @exists
    def dataset_exists(self, dataset_id):
        url = '{b}/dataset/{ds}'.format(b=self.base_url, ds=dataset_id)
        return self.s.head(url, verify=False)

    @http_resp
    def create_dataset(self, dataset):
        url = '{b}/dataset/'.format(b=self.base_url)
        return self.s.post(url, data=dataset.as_json(), verify=False)

    @http_resp
    def update_dataset(self, dataset, old_id=None):
        url = '{b}/dataset/{ds}'.format(b=self.base_url, ds=old_id or dataset.identifier)
        return self.s.post(url, data=dataset.as_json(), verify=False)

    @http_resp
    def delete_dataset(self, dataset):
        url = '{b}/dataset/{ds}'.format(b=self.base_url, ds=dataset.identifier)
        return self.s.delete(url, verify=False)

    @http_resp
    def get_dataset_list(self):
        url = '{b}/dataset/'.format(b=self.base_url)
        return self.s.get(url, params={'all': 1}, verify=False)

    def create_or_update_dataset(self, dataset):
        if self.dataset_exists(dataset.identifier):
            print 'Updating dataset: ' + dataset.identifier
            self.update_dataset(dataset)
        else:
            print 'Creating dataset: ' + dataset.identifier
            self.create_dataset(dataset)

    # @exists
    def activity_exists(self, activity_id):
        url = '{b}/activity/{act}'.format(b=self.base_url, act=activity_id)
        resp = self.s.head(url, verify=False)
        if resp.status_code == 200:
            return True
        else:
            return False

    def get_activity(self, activity_id):
        url = '{b}/activity/{act}'.format(b=self.base_url, act=activity_id)
        resp = self.s.get(url, verify=False)
        try:
            return Activity(resp.json())
        except ValueError:
            raise Exception(resp.text)

    @http_resp
    def create_activity(self, activity):
        url = '{b}/activity/'.format(b=self.base_url)
        return self.s.post(url, data=activity.as_json(), verify=False)

    @http_resp
    def update_activity(self, activity, old_id=None):
        url = '{b}/activity/{act}'.format(b=self.base_url, act=old_id or activity.identifier)
        return self.s.post(url, data=activity.as_json(), verify=False)

    @http_resp
    def delete_activity(self, activity):
        url = '{b}/activity/{act}'.format(b=self.base_url, act=activity.identifier)
        return self.s.delete(url, verify=False)

    def create_or_update_activity(self, activity):
        if self.activity_exists(activity.identifier):
            self.update_activity(activity)
        else:
            self.create_activity(activity)

    def get_activity_list(self):
        url = '{b}/activity'.format(b=self.base_url)

        return self.s.get(url, params={'all': 1}, verify=False).json()

    @exists
    def person_exists(self, person_id):
        url = '{b}/person/{pid}'.format(b=self.base_url, pid=person_id)
        return self.s.head(url, verfiy=False)

    def get_person(self, person_id):
        url = '{b}/person/{pid}'.format(b=self.base_url, pid=person_id)
        resp = self.s.get(url, verify=False)
        try:
            return Person(resp.json())
        except ValueError:
            raise Exception(resp.text)

    def lookup_person(self, name):
        url = '{b}/autocomplete'.format(b=self.base_url)
        resp = self.s.get(url, params={'q': name, 'items': 15, 'type': 'person'}, verify=False)

        if resp.status_code == 200:
            return [re.match(r'\[person\] \{(\d+)\} (.*)', r).groups() for r in resp.json()]
        else:
            raise Exception(resp.text)

    @http_resp
    def create_person(self, person):
        url = '{b}/person/'.format(b=self.base_url)
        return self.s.post(url, data=person.as_json(), verify=False)

    @http_resp
    def update_person(self, person, old_id=None):
        url = '{b}/person/{pid}'.format(b=self.base_url, pid=old_id or person.identifier)
        return self.s.post(url, data=person.as_json(), verify=False)

    @http_resp
    def delete_person(self, person):
        url = '{b}/person/{pid}'.format(b=self.base_url, pid=person.identifier)
        return self.s.delete(url, verify=False)

    @exists
    def article_exists(self, article_id):
        url = '{b}/article/{aid}'.format(b=self.base_url, aid=article_id)
        return self.s.head(url, verify=False)

    def get_article(self, article_id):
        url = '{b}/article/{aid}'.format(b=self.base_url, aid=article_id)
        resp = self.s.get(url, verify=False)
        try:
            return Article(resp.json())
        except ValueError:
            raise Exception(resp.text)

    @http_resp
    def create_article(self, article):
        url = '{b}/article/'.format(b=self.base_url)
        return self.s.post(url, data=article.as_json(), verify=False)

    @http_resp
    def update_article(self, article):
        url = '{b}/article/{aid}'.format(b=self.base_url, aid=article.identifier)
        return self.s.post(url, data=article.as_json(), verify=False)

    @http_resp
    def delete_article(self, article):
        url = '{b}/article/{aid}'.format(b=self.base_url, aid=article.identifier)
        return self.s.delete(url, verify=False)

    @exists
    def webpage_exists(self, webpage_id):
        url = '{b}/webpage/{id}'.format(b=self.base_url, id=webpage_id)
        return self.s.head(url, verify=False)

    def get_webpage(self, webpage_id):
        url = '{b}/webpage/{id}'.format(b=self.base_url, id=webpage_id)
        resp = self.s.get(url, verify=False)
        try:
            return Webpage(resp.json())
        except ValueError:
            raise Exception(resp.text)

    @http_resp
    def create_webpage(self, webpage):
        url = '{b}/webpage/'.format(b=self.base_url)
        return self.s.post(url, data=webpage.as_json(), verify=False)

    @http_resp
    def update_webpage(self, webpage):
        url = '{b}/webpage/{aid}'.format(b=self.base_url, aid=webpage.identifier)
        return self.s.post(url, data=webpage.as_json(), verify=False)

    @http_resp
    def delete_webpage(self, webpage):
        url = '{b}/webpage/{aid}'.format(b=self.base_url, aid=webpage.identifier)
        return self.s.delete(url, verify=False)

    @exists
    def organization_exists(self, org_id):
        url = '{b}/organization/{org_id)'.format(b=self.base_url, org_id=org_id)
        return self.s.head(url, verify=False)

    def get_organization(self, org_id):
        url = '{b}/organization/{org_id}'.format(b=self.base_url, org_id=org_id)
        resp = self.s.get(url, verify=False)

        try:
            return Organization(resp.json())
        except ValueError:
            raise Exception(resp.text)

    def lookup_organization(self, name):
        url = '{b}/autocomplete'.format(b=self.base_url)
        resp = self.s.get(url, params={'q': name, 'items': 15, 'type': 'organization'}, verify=False)
        
        if resp.status_code == 200:
            return [re.match(r'\[organization\] \{(.*)\} (.*)', r).groups() for r in resp.json()]
        else:
            raise Exception(resp.text)

    @http_resp
    def create_organization(self, org):
        url = '{b}/organization/'.format(b=self.base_url)
        return self.s.post(url, data=org.as_json(), verify=False)

    @http_resp
    def update_organization(self, org, old_id=None):
        url = '{b}/organization/{org_id}'.format(b=self.base_url, org_id=old_id or org.identifier)
        return self.s.post(url, data=org.as_json(), verify=False)

    @http_resp
    def delete_organization(self, org):
        url = '{b}/organization/{org_id}'.format(b=self.base_url, org_id=org.identifier)
        return self.s.delete(url, verify=False)

    @http_resp
    def associate_contributor_with_figure(self, contrib, report_id, chapter_id, figure_id):
        url = '{b}/report/{rpt}/chapter/{chp}/figure/contributors/{fig}'.format(b=self.base_url, rpt=report_id, chp=chapter_id, fig=figure_id)

        try:
            data = {
                'role': contrib.role.type_id,
            }
        except AttributeError as e:
            print 'Contributor {c} missing role'.format(c=contrib)
            raise e

        if contrib.person is not None and contrib.person.id is not None:
            data['person_id'] = contrib.person.id
        if contrib.organization is not None and contrib.organization.identifier:
            data['organization_identifier'] = contrib.organization.identifier

        resp = self.s.post(url, data=json.dumps(data), verify=False)
        return resp

    @http_resp
    def delete_contributor_figure_assoc(self, contrib, report_id, chapter_id, figure_id):
        url = '{b}/report/{rpt}/chapter/{chp}/figure/contributors/{fig}'.format(b=self.base_url, rpt=report_id, chp=chapter_id, fig=figure_id)

        data = {
            'delete_contributor': contrib.id
        }

        return self.s.post(url, data=json.dumps(data), verify=False)

    @http_resp
    def associate_contributor_with_image(self, contrib, image_id):
        url = '{b}/image/contributors/{img}'.format(b=self.base_url, img=image_id)

        data = {
            'role': contrib.role.type_id,
        }
        if contrib.person is not None and contrib.person.id is not None:
            data['person_id'] = contrib.person.id
        if contrib.organization is not None and contrib.organization.identifier:
            data['organization_identifier'] = contrib.organization.identifier

        return self.s.post(url, data=json.dumps(data), verify=False)

    @http_resp
    def delete_contributor_image_assoc(self, contrib, image_id):
        url = '{b}/image/contributors/{img}'.format(b=self.base_url, img=image_id)

        data = {
            'delete': {
                'role': contrib.role.type_id,
                'organization_identifier': contrib.organization.identifier,
                'person_id': contrib.person.identifier
            }
        }

        return self.s.post(url, data=json.dumps(data), verify=False)

    @http_resp
    def associate_figure_with_parent(self, report_id, figure_id, parent, activity_id=None):
        url = '{b}/report/{rpt}/figure/prov/{fig}'.format(b=self.base_url, rpt=report_id, fig=figure_id)

        data = {
            'parent_uri': parent.url,
            'parent_rel': parent.relationship
        }
        if activity_id:
            data['activity'] = activity_id

        try:
            self.delete_figure_parent_assoc(report_id, figure_id, parent)
        except AssociationException as e:
            print e.value

        resp = self.s.post(url, data=json.dumps(data), verify=False)
        return resp

    def delete_figure_parent_assoc(self, report_id, figure_id, parent):
        url = '{b}/report/{rpt}/figure/prov/{fig}'.format(b=self.base_url, rpt=report_id, fig=figure_id)

        data = {
            'delete': {
                'parent_uri': parent.url,
                'parent_rel': parent.relationship
            }
        }
        resp = self.s.post(url, data=json.dumps(data), verify=False)

        if resp.status_code == 200:
            return resp
        else:
            raise AssociationException(
                'Parent dissociation failed:\n{url}\n{resp}\n{d}'.format(url=url, resp=resp.text, d=data))

    @http_resp
    def associate_image_with_parent(self, image_id, parent, activity_id=None):
        url = '{b}/image/prov/{img}'.format(b=self.base_url, img=image_id)

        data = {
            'parent_uri': parent.url,
            'parent_rel': parent.relationship
        }
        if activity_id:
            data['activity'] = activity_id

        try:
            self.delete_dataset_image_assoc(image_id, parent)
        except AssociationException as e:
            print e.value

        resp = self.s.post(url, data=json.dumps(data), verify=False)
        return resp

    def delete_dataset_image_assoc(self, image_id, parent):
        url = '{b}/image/prov/{img}'.format(b=self.base_url, img=image_id)

        data = {
            'delete': {
                'parent_uri': parent.url,
                'parent_rel': parent.relationship
            }
        }
        resp = self.s.post(url, data=json.dumps(data), verify=False)

        if resp.status_code == 200:
            return resp
        else:
            raise AssociationException(
                'Parent dissociation failed:\n{url}\n{resp}\n{d}'.format(url=url, resp=resp.text, d=data))

    def lookup_publication(self, pub_type, name):
        url = '{b}/autocomplete'.format(b=self.base_url)
        resp = self.s.get(url, params={'q': name, 'items': 15, 'type': pub_type}, verify=False)

        if resp.status_code == 200:
            return [re.match(r'\[.+\] \{(.+)\} (.*)', r).groups() for r in resp.json()]
            # return resp.json()
        else:
            raise Exception('Lookup failed:\nQuery:{q}\nType:{t}\nResponse:\n{r}'.format(q=name, t=pub_type, r=resp.text))



