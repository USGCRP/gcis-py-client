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

PARENT_TRANSLATIONS = {
    'what_type_of_publication_was_the_figure_published_in': 'publication_type_identifier',
    'name_title': 'label',
    'article_title': 'label',
    'book_title': 'label',
    'web_page_title': 'label',
    'conference_title': 'label',
    'title': 'label',
    }