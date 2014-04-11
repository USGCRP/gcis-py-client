__author__ = 'abuddenberg'
from os.path import exists


#This function is for adding images to existing figures
def move_images_to_gcis(webform_client, gcis_client, webform_url, gcis_id, report_id, subset_images=None):
    figure = webform_client.get_webform(webform_url, download_images=True)
    #Now identifiers don't need to be matched
    figure.identifier = gcis_id

    #If a subset of identifiers has been provided, only process those
    if subset_images:
        images_to_process = [image for image in figure.images if image.identifier in subset_images]
    else:
        images_to_process = figure.images

    for image in images_to_process:
        if not exists(image.local_path):
            raise Exception('Local file missing ' + image.local_path)

        if not gcis_client.image_exists(image.identifier):
            print 'Creating image: {img}'.format(img=image.identifier)
            gcis_client.create_image(image, report_id=report_id, figure_id=figure.identifier)


def sync_dataset_metadata(gcis_client, datasets):
    for ds in datasets:
        gcis_client.create_or_update_dataset(ds)
        gcis_client.create_or_update_activity(ds.activity)


def populate_contributors(gcis_client, contributors):
    for cont in contributors:
        person = cont.person
        org = cont.organization

        matches = gcis_client.lookup_person(person.last_name)
        if len(matches) == 1:
            person.id = matches[0][0]
        elif len(matches) == 0:
            print 'No ID found for ' + person.last_name
        else:
            print 'Ambiguous results for ' + person.last_name
            print '\t', matches