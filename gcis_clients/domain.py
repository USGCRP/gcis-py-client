__author__ = 'abuddenberg'

from copy import deepcopy
import json
import re
import inspect

from dateutil.parser import parse


class Gcisbase(object):
    def __init__(self, data, fields=[], trans={}):
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
                    setattr(self, k, data[k])

    def merge(self, other):
        #This sucks
        attrs_we_care_about = [(attr, v) for attr, v in inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
                               if not attr.startswith('__')]

        for attr, value in attrs_we_care_about:
            if value in (None, '') and hasattr(other, attr):
                setattr(self, attr, getattr(other, attr))

        return self

    def as_json(self, indent=0, omit_fields=[]):
        out_fields = set(self.gcis_fields) - (set(['uri', 'href']) | set(omit_fields))
        return json.dumps({f: getattr(self, f) for f in out_fields}, indent=indent)


class GcisObject(Gcisbase):
    def __init__(self, data, **kwargs):
        #Special case for contributors
        contrib_list = data.pop('contributors', None)
        self.contributors = [Contributor(contrib) for contrib in contrib_list] if contrib_list else []

        super(GcisObject, self).__init__(data, **kwargs)

    def add_contributor(self, contributor):
        self.contributors.append(contributor)

    def add_person(self, person):
        self.contributors.append(Contributor(person, Organization()))


class Figure(GcisObject):
    def __init__(self, data):
        self.gcis_fields = [
            'usage_limits', 'kindred_figures', 'time_end', 'keywords', 'lat_min', 'create_dt', 'lat_max', 'time_start',
            'title', 'ordinal', 'lon_min', 'report_identifier', 'chapter', 'submission_dt', 'uri', 'lon_max',
            'caption', 'source_citation', 'attributes', 'identifier', 'chapter_identifier', 'images'
        ]

        self.translations = {
            'what_is_the_figure_id': 'identifier',
            'what_is_the_name_of_the_figure_as_listed_in_the_report': 'title',
            'when_was_this_figure_created': 'create_dt',
            'what_is_the_chapter_and_figure_number': 'figure_num'
        }

        super(Figure, self).__init__(data, fields=self.gcis_fields, trans=self.translations)

        #Special case for chapter
        chap_tree = data.pop('chapter', None)
        self.chapter = Chapter(chap_tree) if chap_tree else self.chapter

        #Special case for images
        image_list = data.pop('images', None)
        self.images = [Image(image) for image in image_list] if image_list else []

        #Hack
        self.identifier = self.identifier.replace('/figure/', '') if self.identifier != '' else '***ID MISSING***'

    @property
    def figure_num(self):
        if isinstance(self.chapter, Chapter) and self.chapter.number and self.ordinal:
            return '{0}.{1}'.format(self.chapter.number, self.ordinal)
        else:
            return '{0}.{1}'.format(self.chapter, self.ordinal)

    #TODO: Ordinal handling is unnecessarily complex
    @figure_num.setter
    def figure_num(self, value):
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

    def as_json(self, indent=0):
        return super(Figure, self).as_json(omit_fields=['images', 'chapter', 'kindred_figures', 'keywords'])

    def __str__(self):
        string = '{f_id}: Figure {f_num}: {f_name}\n\tImages: {imgs}'.format(
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


class Chapter(GcisObject):
    def __init__(self, data):
        self.gcis_fields = ['report_identifier', 'identifier', 'number', 'url', 'title']

        super(Chapter, self).__init__(data, fields=self.gcis_fields)


class Image(GcisObject):
    def __init__(self, data, local_path=None, remote_path=None):
        self.gcis_fields = ['attributes', 'create_dt', 'description', 'identifier', 'lat_max', 'lat_min', 'lon_max',
                            'uri', 'lon_min', 'position', 'submission_dt', 'time_end', 'time_start', 'title', 'href',
                            'usage_limits']

        self.translations = {
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

        #Private attributes for handling date parsing
        self._create_dt = None

        super(Image, self).__init__(data, fields=self.gcis_fields, trans=self.translations)

        #Hack
        self.identifier = self.identifier.replace('/image/', '')

        self.local_path = local_path
        self.remote_path = remote_path

        #This does not accurately reflect GCIS' data model
        self.datasets = []

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
        return 'Image: {id}: {name}'.format(id=self.identifier, name=self.title)


class Dataset(GcisObject):
    def __init__(self, data):
        self.gcis_fields = ['contributors', 'vertical_extent', 'native_id', 'href', 'references', 'cite_metadata',
                        'scale', 'publication_year', 'temporal_extent', 'version', 'parents', 'scope', 'type',
                        'processing_level', 'files', 'data_qualifier', 'access_dt', 'description', 'spatial_ref_sys',
                        'spatial_res', 'spatial_extent', 'doi', 'name', 'url', 'uri', 'identifier', 'release_dt',
                        'attributes']

        self.translations = {
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

        #This desperately needs to get added to the webform
        self._identifiers = {
            'Global Historical Climatology Network - Daily': 'nca3-ghcn-daily-r201305',
            'Global Historical Climatology Network - Monthly': 'nca3-ghcn-monthly-r201305',
            'NCDC Merged Land and Ocean Surface Temperature': 'nca3-mlost',
            'U.S. Climate Divisional Dataset Version 2': 'nca3-cddv2-r1',
            'Climate Division Database Version 2': 'nca3-cddv2-r1',
            'Eighth degree-CONUS Daily Downscaled Climate Projections by Katharine Hayhoe': 'nca3-cmip3-downscaled-r201304',
            'Eighth degree-CONUS Daily Downscaled Climate Projections': 'nca3-cmip3-downscaled-r201304',
            'Earth Policy Institute Atmospheric Carbon Dioxide Concentration, 1000-2012': 'nca3-epi-co2-r201307',
            'Daily 1/8-degree gridded meteorological data [1 Jan 1949 - 31 Dec 2010]': 'nca3-maurer-r201304',
            'NCEP/NCAR Reanalysis': 'nca3-ncep-ncar-r1',
            'NCDC Global Surface Temperature Anomalies': 'nca3-ncdc-gst-anomalies-r201307',
            'GRACE Static Field Geopotential Coefficients JPL Release 5.0 GSM': 'nca3-grace-r201307',
            'UW/NCDC Satellite Derived Hurricane Intensity Dataset': 'nca3-hurricane-intensity-r1',
            'Bias-Corrected and Spatially Downscaled Surface Water Projections Hydrologic Data': 'nca3-water-projections-r201208',
            'International Best Track Archive for Climate Stewardship (IBTrACS)': 'nca3-ibtracs-r201311',
            'the World Climate Research Programme\'s (WCRP\'s) Coupled Model Intercomparison Project phase 3 (CMIP3) multi-model dataset': 'nca3-cmip3-r201205',
            'World Climate Research Programme\'s (WCRP\'s) Coupled Model Intercomparison Project phase 3 (CMIP3) multi-model dataset': 'nca3-cmip3-r201205',
            'World Climate Research Program\'s (WCRP\'s) Coupled Model Intercomparison Project phase 3 (CMIP3) multi-model dataset': 'nca3-cmip3-r201205',
            'North American Regional Climate Change Assessment Program dataset': 'nca3-narccap-r201205',
            'Gridded Population of the World Version 3 (GPWv3): Population Count Grid': 'nca3-gpwv3-r201211',
            'ETCCDI Extremes Indices Archive': 'nca3-etccdi-r201305',
            'Historical Climatology Network Monthly (USHCN) Version 2.5': 'nca3-ushcn',
            'Annual Maximum Ice Coverage (AMIC)': 'nca3-amic-r201308',
            'Global Historical Climatology Network-Daily (GHCN-D) Monthly Summaries: North American subset': 'nca3-ghcnd-monthly-summaries-r201401',
            'Global Sea Level From TOPEX & Jason Altimetry': 'nca3-topex-jason-altimetry-r1',
            'World Climate Research Program\'s (WCRP\'s) Coupled Model Intercomparison Project phase 5 (CMIP5) multi-model ensemble': 'nca3-cmip5-r1',

            #Surely we can do better
            'Proxy Data': 'nca3-proxy-data-r1',
            'Tide Gauge Data': 'nca3-tide-gauge-data-r1',
            'Projected Sea Level Rise': 'nca3-projected-sea-level-rise-r1',
        }

        #Private attributes for handling date parsing
        self._release_dt = None
        self._access_dt = None
        self._publication_year = None

        #These do not accurately reflect GCIS' data model
        self.note = None
        self.activity = None

        super(Dataset, self).__init__(data, fields=self.gcis_fields, trans=self.translations)

        self.identifier = self._identifiers[self.name] if self.name in self._identifiers else self.name

    def __repr__(self):
        return 'Dataset: {id}: {name}'.format(id=self.identifier, name=self.name)

    def __str__(self):
        return self.__repr__()

    def as_json(self, indent=0):
        return super(Dataset, self).as_json(omit_fields=['files', 'parents', 'contributors', 'references'])

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

    @property
    def publication_year(self):
        return self._publication_year

    @publication_year.setter
    def publication_year(self, value):
        match = re.search('\d{4}', value) if value else None
        if match:
            self._publication_year = match.group()
        else:
            self._publication_year = None
            
            
class Activity(GcisObject):
    def __init__(self, data):
        self.gcis_fields = ['start_time', 'uri', 'methodology', 'data_usage', 'href', 'metholodogies', 'end_time',
                            'output_artifacts', 'duration', 'identifier', 'publication_maps', 'computing_environment',
                            'software', 'visualization_software', 'notes']

        self.translations = {
            'how_much_time_was_invested_in_creating_the_image': 'duration',
            '35_what_are_all_of_the_files_names_and_extensions_associated_with_this_image': 'output_artifacts',
            'what_operating_systems_and_platforms_were_used': 'computing_environment',
            'what_analytical_statistical_methods_were_employed_to_the_data': 'methodology',
            'describe_how_the_data_was_used_in_the_image_figure_creation': 'data_usage',
            'list_the_name_and_version_of_the_software': 'software',
            'what_software_applications_were_used_to_manipulate_the_data': 'notes',
            '33_what_software_applications_were_used_to_visualize_the_data': 'visualization_software'

        }

        super(Activity, self).__init__(data, fields=self.gcis_fields, trans=self.translations)

    def as_json(self, indent=0):
        return super(Activity, self).as_json(omit_fields=['metholodogies', 'publication_maps'])

    def __repr__(self):
        return 'Activity: {id}'.format(id=self.identifier)

    def __str__(self):
        return self.__repr__()


class Person(Gcisbase):
    def __init__(self, data):
        self.gcis_fields = ['first_name', 'last_name', 'middle_name', 'contributors', 'url', 'uri', 'href', 'orcid',
                            'id']

        self.translations = {}

        super(Person, self).__init__(data, fields=self.gcis_fields, trans=self.translations)

    def as_json(self, indent=0):
        return super(Person, self).as_json(omit_fields=['contributors'])

    def __repr__(self):
        return 'Person: {id}: {fn} {ln}'.format(id=self.id, fn=self.first_name, ln=self.last_name)

    def __str__(self):
        return self.__repr__()


class Organization(Gcisbase):
    def __init__(self, data):
        self.gcis_fields = ['organization_type_identifier', 'url', 'uri', 'href', 'country_code', 'identifier', 'name']

        self.translations = {}

        self._identifiers = {
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
            'University of Alaska': 'university-alaska'


        }

        super(Organization, self).__init__(data, fields=self.gcis_fields, trans=self.translations)
        
        self.identifier = self._identifiers[self.name] if self.name in self._identifiers else None

    def __repr__(self):
        return 'Organization: {id}: {name}'.format(id=self.identifier, name=self.name)

    def __str__(self):
        return self.__repr__()


class Contributor(Gcisbase):
    def __init__(self, data):
        self.gcis_fields = ['role_type_identifier', 'organization_uri', 'uri', 'href', 'person_uri']

        #Hack
        self.people_role_map = {
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
            ' Chapin': 'scientist'
        }

        super(Contributor, self).__init__(data, fields=self.gcis_fields)

        self.person = None
        self.organization = None
        self._role = None

    @property
    def role(self):

        #Hack hack hack
        if self._role is None:
            horrible_key = ' '.join((self.person.first_name, self.person.last_name))
            self._role = Role(self.people_role_map[horrible_key]) if horrible_key in self.people_role_map else None

        return self._role

    def __repr__(self):
        return '({p}/{o}/{r})'.format(p=self.person, o=self.organization, r=self.role)

    def __str__(self):
        return self.__repr__()


class Role(object):
    def __init__(self, type_id):
        self.type_id = type_id

    def __repr__(self):
        return self.type_id

    def __str__(self):
        return self.__repr__()

