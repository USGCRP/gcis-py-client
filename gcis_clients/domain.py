__author__ = 'abuddenberg'

from copy import deepcopy
import json
import re
import inspect

from dateutil.parser import parse


class Gcisbase(object):
    def __init__(self, data, fields=(), trans=()):
        #Setup class variables
        self.gcis_fields = fields
        self.translations = trans

        #Save off a copy of the original JSON for debugging
        self.original = deepcopy(data)

        #Create attributes from the master list
        self. __dict__.update(dict.fromkeys(self.gcis_fields, None))

        #Perform translations
        for term in self.translations:
            val = data.pop(term, None)
            if val is not None:
                data[self.translations[term]] = val

        for k in data:
            if hasattr(self, k):
                try:
                    #Strip whitespace from strings for consistency
                    data[k] = data[k].strip()

                    #We now have unicode characters infesting our data.  I'm sure this is wrong.
                    data[k] = data[k].encode('utf-8')
                except AttributeError:
                    pass
                finally:
                    if data[k]:
                        setattr(self, k, data[k])

    def merge(self, other):
        #This sucks
        attrs_we_care_about = [(attr, v) for attr, v in inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
                               if not attr.startswith('__')]

        for attr, value in attrs_we_care_about:
            if value in (None, '') and hasattr(other, attr):
                setattr(self, attr, getattr(other, attr))

        return self

    def as_json(self, indent=0, omit_fields=()):
        out_fields = set(self.gcis_fields) - (set(['uri', 'href']) | set(omit_fields))
        return json.dumps({f: getattr(self, f) for f in out_fields}, indent=indent)


class GcisObject(Gcisbase):
    def __init__(self, data, **kwargs):
        if type(data) is not dict:
            raise TypeError('Expected dict, got {t}'.format(t=type(data)))

        #Special case for contributors
        contrib_list = data.pop('contributors', None)
        self.contributors = [Contributor(contrib) for contrib in contrib_list] if contrib_list else []

        parents_list = data.pop('parents', None)
        self.parents = [Parent(parent) for parent in parents_list] if parents_list else []

        super(GcisObject, self).__init__(data, **kwargs)

    def add_contributor(self, contributor):
        if isinstance(contributor, Contributor):
            self.contributors.append(contributor)
        else:
            raise TypeError('Expected Contributor, got {t}'.format(t=type(contributor)))

    def add_person(self, person):
        self.contributors.append(Contributor(person, Organization()))

    def add_parent(self, parent):
        if isinstance(parent, Parent):
            self.parents.append(parent)
        else:
            raise TypeError('Expected Parent, got {t}'.format(t=type(parent)))


class Figure(GcisObject):
    def __init__(self, data, local_path=None, remote_path=None, trans=()):
        self.gcis_fields = [
            'usage_limits', 'kindred_figures', 'time_start', 'time_end', 'keywords', 'lat_min', 'create_dt', 'lat_max',
            'title', 'ordinal', 'lon_min', 'report_identifier', 'chapter', 'submission_dt', 'uri', 'lon_max',
            'caption', 'source_citation', 'attributes', 'identifier', 'chapter_identifier', 'images', 'url'
        ]

        super(Figure, self).__init__(data, fields=self.gcis_fields, trans=trans)

        self.local_path = local_path
        self.remote_path = remote_path

        #Special case for chapter
        chap_tree = data.pop('chapter', None)
        self.chapter = Chapter(chap_tree) if chap_tree else self.chapter

        #Special case for images
        image_list = data.pop('images', None)
        self.images = [Image(image) for image in image_list] if image_list else []

        file_list = data.pop('files', None)
        self.files = [File(f) for f in file_list] if file_list else []

        #Hack
        self.identifier = self.identifier.replace('/figure/', '') if self.identifier not in ('', None) else '***ID MISSING***'

    @property
    def figure_num(self):
        if isinstance(self.chapter, Chapter) and self.chapter.number and self.ordinal:
            return '{0}.{1}'.format(self.chapter.number, self.ordinal)
        else:
            return '{0}.{1}'.format(self.chapter, self.ordinal)

    #TODO: Ordinal handling is unnecessarily complex
    @figure_num.setter
    def figure_num(self, value):
        if value:
            try:
                chp, fig = value.split('.')
                chp = int(chp)
                fig = int(fig)
            except ValueError:
                print 'Invalid chapter/figure numbers: ' + value
                chp = None
                fig = None
            self.ordinal = fig

            #If we have an actual Chapter instance, populate it
            if isinstance(self.chapter, Chapter):
                self.chapter.number = chp
            else:
                self.chapter = chp

    def as_json(self, indent=0, omit_fields=('images', 'chapter', 'kindred_figures', 'keywords')):
        return super(Figure, self).as_json(omit_fields=omit_fields)

    def __str__(self):
        string = '<Figure: id:{f_id} fignum:{f_num} name:{f_name}>\n\t[Images: {imgs}]'.format(
            f_id=self.identifier, f_num=self.figure_num, f_name=self.title, imgs=[i.identifier for i in self.images]
        )
        return string

    def __repr__(self):
        # return super(Figure, self).__repr__()
        return self.__str__()

    def merge(self, other):
        # Special handling for Chapters
        if isinstance(other.chapter, Chapter) and isinstance(self.chapter, Chapter):
            self.chapter.merge(other.chapter)

        #This might want to move to Chapter's merge()
        elif isinstance(other.chapter, Chapter) and not isinstance(self.chapter, Chapter):
            chapter_num = self.chapter
            self.chapter = other.chapter
            self.chapter.number = chapter_num

        return super(Figure, self).merge(other)


class Report(GcisObject):
    def __init__(self, data, trans=()):
        self.gcis_fields = ['doi', 'contact_note', 'title', 'publication_year', 'summary', 'url', 'contact_email', 'identifier', 'report_type_identifier']

        super(Report, self).__init__(data, fields=self.gcis_fields, trans=trans)

        # if self.report_type_identifier not in ['report', 'assessment', 'technical_input', 'indicator']:
        #     raise ValueError("report_type_identifier must be one of 'report', 'assessment', 'technical_input', 'indicator'")

    def as_json(self, indent=0, omit_fields=()):
        return super(Report, self).as_json(omit_fields=omit_fields)

    def __repr__(self):
        return '<Report: id:{id}>'.format(id=self.identifier)

    def __str__(self):
        return self.__repr__()


class Chapter(GcisObject):
    def __init__(self, data):
        self.gcis_fields = ['report_identifier', 'identifier', 'number', 'url', 'title']

        super(Chapter, self).__init__(data, fields=self.gcis_fields)

    def as_json(self, indent=0, omit_fields=()):
        return super(Chapter, self).as_json(omit_fields=omit_fields)

    def __repr__(self):
        return '<Chapter: id:{id}>'.format(id=self.identifier)

    def __str__(self):
        return self.__repr__()


class Image(GcisObject):
    def __init__(self, data, local_path=None, remote_path=None, trans=()):
        self.gcis_fields = ['attributes', 'create_dt', 'description', 'identifier', 'lat_max', 'lat_min', 'lon_max',
                            'uri', 'lon_min', 'position', 'submission_dt', 'time_end', 'time_start', 'title', 'href',
                            'usage_limits']

        #Private attributes for handling date parsing
        self._create_dt = None

        super(Image, self).__init__(data, fields=self.gcis_fields, trans=trans)

        self.local_path = local_path
        self.remote_path = remote_path

    @property
    def create_dt(self):
        return self._create_dt

    @create_dt.setter
    def create_dt(self, value):
        try:
            self._create_dt = parse(value).isoformat() if value else None
        except TypeError:
            self._create_dt = None

    def __str__(self):
        return '<Image: id:{id} name:{name}>'.format(id=self.identifier, name=self.title)


class Dataset(GcisObject):
    def __init__(self, data, trans=(), known_ids=None):
        self.gcis_fields = ['contributors', 'vertical_extent', 'native_id', 'href', 'references', 'cite_metadata',
                            'scale', 'publication_year', 'temporal_extent', 'version', 'parents', 'scope', 'type',
                            'processing_level', 'files', 'data_qualifier', 'access_dt', 'description',
                            'spatial_ref_sys', 'spatial_res', 'spatial_extent', 'doi', 'name', 'url', 'uri',
                            'identifier', 'release_dt', 'attributes']

        #TODO: This hack has got to go.
        self._identifiers = known_ids

        #Private attributes for handling date parsing
        self._release_dt = None
        self._access_dt = None
        self._publication_year = None

        super(Dataset, self).__init__(data, fields=self.gcis_fields, trans=trans)

        self.identifier = self._identifiers[self.name] if self._identifiers and self.name in self._identifiers else self.identifier

    def __repr__(self):
        return '<Dataset: id:{id} name:{name}>'.format(id=self.identifier, name=self.name)

    def __str__(self):
        return self.__repr__()

    def as_json(self, indent=0, omit_fields=('files', 'parents', 'contributors', 'references')):
        return super(Dataset, self).as_json(omit_fields=omit_fields)

    def merge(self, other):
        for k in self.__dict__:
            #If our copy of the field is empty or the other copy is longer, take that one.
            #TODO: Shoot myself for professional negligence.
            if hasattr(other, k) and (self.__dict__[k] in (None, '') or len(getattr(other, k)) > self.__dict__[k]):
                self.__dict__[k] = getattr(other, k)
            return self

    @property
    def release_dt(self):
        return self._release_dt

    @release_dt.setter
    def release_dt(self, value):
        try:
            self._release_dt = parse(value).isoformat() if value else None
        except TypeError:
            self._release_dt = None
        except ValueError:
            self._release_dt = None

    @property
    def access_dt(self):
        return self._access_dt

    @access_dt.setter
    def access_dt(self, value):
        try:
            self._access_dt = parse(value).isoformat() if value else None
        except TypeError:
            # print "Problem with date: " + self.access_dt
            self._access_dt = None
        except ValueError:
           self._access_dt = None

    @property
    def publication_year(self):
        return self._publication_year

    @publication_year.setter
    def publication_year(self, value):
        match = re.search('\d{4}', str(value)) if value else None
        if match:
            self._publication_year = match.group()
        else:
            self._publication_year = None
            
            
class Activity(GcisObject):
    def __init__(self, data, trans=()):
        self.gcis_fields = ['start_time', 'uri', 'methodology', 'data_usage', 'href', 'metholodogies', 'end_time',
                            'output_artifacts', 'duration', 'identifier', 'publication_maps', 'computing_environment',
                            'software', 'visualization_software', 'notes']

        super(Activity, self).__init__(data, fields=self.gcis_fields, trans=trans)

    def as_json(self, indent=0, omit_fields=('metholodogies', 'publication_maps')):
        return super(Activity, self).as_json(omit_fields=omit_fields)

    def __repr__(self):
        return '<Activity: id:{id}>'.format(id=self.identifier)

    def __str__(self):
        return self.__repr__()


class Person(Gcisbase):
    def __init__(self, data, trans=()):
        self.gcis_fields = ['first_name', 'last_name', 'middle_name', 'contributors', 'url', 'uri', 'href', 'orcid',
                            'id']

        super(Person, self).__init__(data, fields=self.gcis_fields, trans=trans)

    def as_json(self, indent=0, omit_fields=('contributors',)):
        return super(Person, self).as_json(omit_fields=omit_fields)

    def __repr__(self):
        return '<Person: id:{id} first:{fn} last:{ln}>'.format(id=self.id, fn=self.first_name, ln=self.last_name)

    def __str__(self):
        return self.__repr__()


class Organization(Gcisbase):
    def __init__(self, data, trans=()):
        self.gcis_fields = ['organization_type_identifier', 'url', 'uri', 'href', 'country_code', 'identifier', 'name']

        super(Organization, self).__init__(data, fields=self.gcis_fields, trans=trans)

    def __repr__(self):
        return '<Organization: id:{id} name:{name}>'.format(id=self.identifier, name=self.name)

    def __str__(self):
        return self.__repr__()


class Contributor(Gcisbase):
    def __init__(self, data):
        self.gcis_fields = ['role_type_identifier', 'organization_uri', 'uri', 'href', 'person_uri', 'person_id', 'id']

        super(Contributor, self).__init__(data, fields=self.gcis_fields)

        person_tree = data.pop('person', None)
        org_tree = data.pop('organization', None)

        self.person = Person(person_tree) if person_tree else None
        self.organization = Organization(org_tree) if org_tree else None
        self.role = Role(self.role_type_identifier) if self.role_type_identifier else None

    def __repr__(self):
        return '<Contributor: Person:{p} Org:{o} Role:{r}>'.format(p=self.person, o=self.organization, r=self.role)

    def __str__(self):
        return self.__repr__()


class Role(object):
    def __init__(self, type_id):
        self.type_id = type_id

    def __repr__(self):
        return self.type_id

    def __str__(self):
        return self.__repr__()


class Parent(Gcisbase):
    def __init__(self, data, target_pub=None, trans=(), pubtype_map=None):
        self.gcis_fields = ['relationship', 'url', 'publication_type_identifier', 'label', 'activity_uri', 'note']

        self.publication_type_map = pubtype_map

        self._publication_type_identifier = None

        self.activity = None

        super(Parent, self).__init__(data, fields=self.gcis_fields, trans=trans)
        self.publication = target_pub

        #HACK: Set default relationship type
        self.relationship = self.relationship if self.relationship else 'prov:wasDerivedFrom'

    @property
    def publication_type_identifier(self):
        return self._publication_type_identifier

    @publication_type_identifier.setter
    def publication_type_identifier(self, value):
        self._publication_type_identifier = self.publication_type_map[value] \
            if self.publication_type_map and value in self.publication_type_map else value

    @staticmethod
    def from_obj(gcis_obj, activity=None):
        gcis_obj_type = type(gcis_obj).__name__.lower()

        if hasattr(gcis_obj, 'title'):
            label = gcis_obj.title
        elif hasattr(gcis_obj, 'name'):
            label = gcis_obj.name
        else:
            label = '***MISSING***'

        p = Parent({
            'relationship': 'prov:wasDerivedFrom',
            'publication_type_identifier': gcis_obj_type,
            'url': '/{type}/{id}'.format(type=gcis_obj_type, id=gcis_obj.identifier) if gcis_obj_type and gcis_obj.identifier else None,
            'label': label
        }, target_pub=gcis_obj)
        p.activity = activity

        return p

    def __repr__(self):
        return '<Parent: rel:{rel} pub_type:{type} url:{url} label:{lbl}>'.format(
            rel=self.relationship, type=self.publication_type_identifier, url=self.url, lbl=self.label
        )

    def __str__(self):
        return self.__repr__()


class Article(Gcisbase):
    def __init__(self, data, trans=()):
        self.gcis_fields = ['files', 'doi', 'contributors', 'title', 'url', 'notes', 'uri',
                            'journal_identifier', 'journal_pages', 'cited_by', 'href', 'parents', 'year',
                            'journal_vol', 'references', 'identifier']

        super(Article, self).__init__(data, fields=self.gcis_fields, trans=trans)

    def as_json(self, indent=0, omit_fields=('files', 'parents', 'contributors', 'references', 'cited_by')):
        return super(Article, self).as_json(omit_fields=omit_fields)

    def __repr__(self):
        return '<Article: id:{id} title:{t}>'.format(id=self.identifier, t=self.title)

    def __str__(self):
        return self.__repr__()


class Webpage(Gcisbase):
    def __init__(self, data, trans=()):
        self.gcis_fields = ['files', 'contributors', 'title', 'url', 'uri', 'cited_by', 'href', 'references',
                            'parents', 'access_date', 'identifier']

        super(Webpage, self).__init__(data, fields=self.gcis_fields, trans=trans)

    def as_json(self, indent=0, omit_fields=('files', 'parents', 'contributors', 'references', 'cited_by')):
        return super(Webpage, self).as_json(omit_fields=omit_fields)

    def __repr__(self):
        return '<Webpage id:{id} title:{t}>'.format(id=self.identifier, t=self.title)

    def __str__(self):
        return self.__repr__()


class File(Gcisbase):
    def __init__(self, data, trans=()):
        self.gcis_fields = ['landing_page', 'sha1', 'url', 'thumbnail_href', 'uri', 'href', 'location', 'file', 'identifier', 'thumbnail', 'mime_type', 'size']

        super(File, self).__init__(data, fields=self.gcis_fields, trans=trans)

    # def as_json(self, indent=0, omit_fields=('files', 'parents', 'contributors', 'references', 'cited_by')):
    #     return super(File, self).as_json(omit_fields=omit_fields)

    def __repr__(self):
        return '<File id:{id} path:{p}>'.format(id=self.identifier, p=self.file)

    def __str__(self):
        return self.__repr__()
