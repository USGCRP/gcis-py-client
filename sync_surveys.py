__author__ = 'abuddenberg'

from gcis_clients import GcisClient, SurveyClient, survey_token, gcis_dev_auth
from gcis_clients.domain import Report, Chapter
from sync_utils import realize_parents, realize_contributors

from collections import OrderedDict

import pickle


gcis = GcisClient('http://data.gcis-dev-front.joss.ucar.edu', *gcis_dev_auth)
surveys = SurveyClient('https://healthresources.globalchange.gov', survey_token)

sync_metadata_tree = {
    'usgcrp-climate-and-health-assessment-draft': OrderedDict([
        ('executive-summary', []),
        ('climate-change-and-human-health', [
            ('/metadata/figures/3698', 'major_u_s__climate_trends'), #1.1 #climate-change-and-human-health
            ('/metadata/figures/3632', 'percent_changes_in_the_annual_number_of_extreme_precipitation_events_'), #1.2 #climate-change-and-human-health
            ('/metadata/figures/3635', 'projected_changes_in_temperature_and_precipitation_by_mid_century'), #1.3 #climate-change-and-human-health
            ('/metadata/figures/3633', 'projected_changes_in_the_hottest_coldest_and_wettest_driest_day_of_the_year'), #1.4 #climate-change-and-human-health
            ('/metadata/figures/3757', 'climate_change_and_health'), #1.5 #climate-change-and-human-health
        ]),
        ('temperature-related-death-and-illness', [
            ('/metadata/figures/3811', 'climate_change_and_health__extreme_heat'), #2.1 #temperature-related-death-and-illness
            ('/metadata/figures/3585', 'heat_related_deaths_during_the_1995_chicago_heat_wave'), #2.2 #temperature-related-death-and-illness
            ('/metadata/figures/3643', 'projected_net_changes_in_extreme_temperature_related_deaths'), #2.3 #temperature-related-death-and-illness
            ('/metadata/figures/3653', 'projected_changes_in_deaths_in_u_s__cities_by_season'), #2.4 #temperature-related-death-and-illness
        ]),
        ('air-quality-impacts', [
            ('/metadata/figures/3812', 'climate_change_and_health__outdoor_air_quality'), #3.1 #air-quality-impacts
            ('/metadata/figures/3647', 'projected_change_in_average_daily_maximum_temperature__seasonal_average_maximum_daily_8_hr_ozone__and_ozone_related_premature_deaths_in_2013'), #3.2 #air-quality-impacts
            ('/metadata/figures/3649', 'projected_change_in_ozone_related_premature_deaths'), #3.3 #air-quality-impacts
            ('/metadata/figures/3650', 'ragweed_pollen_season_lengthens'), #3.4 #air-quality-impacts
        ]),
        ('vectorborne-diseases', [
            ('/metadata/figures/3807', 'climate_change_and_health__lyme_disease'), #4.1 #vectorborne-diseases
            ('/metadata/figures/3659', 'changes_in_lyme_disease_case_report_distribution'), #4.2 #vectorborne-diseases
            ('/metadata/figures/3658', 'life_cycle_of_blacklegged_ticks__ixodes_scapularis'), #4.3 #vectorborne-diseases
            ('/metadata/figures/3747', 'lyme_disease_onset_week_modeling_scenarios'), #4.4 #vectorborne-diseases
            ('/metadata/figures/3674', 'incidence_of_west_nile_neuroinvasive_disease_in_the_united_states'), #4.5 #vectorborne-diseases
            ('/metadata/figures/3675', 'climate_impacts_on_west_nile_virus_transmission'), #4.6 #vectorborne-diseases
        ]),
        ('water-related-illnesses', [
            ('/metadata/figures/3824', 'climate_change_and_health___vibrio'), #5.1 #water-related-illnesses
            ('/metadata/figures/3700', 'links_between_climate_change__water_quantity_and_quality__and_human_exposure_to_water_related_illness'), #5.2 #water-related-illnesses
            ('/metadata/figures/3671', 'locations_of_livestock_and_projections_of_heavy_precipitation'), #5.3 #water-related-illnesses
            # ('/metadata/figures/3673', 'potential_routes_of_manure_borne_microbial_contaminants_to_ground_and_surface_water_supplies_'), #5.3 #water-related-illnesses UNUSED?
            ('/metadata/figures/3709', 'projections_of_vibrio_occurrence_and_abundance_in_chesapeake_bay'), #5.4 #water-related-illnesses
            ('/metadata/figures/3704', 'changes_in_suitable_coastal_vibrio_habitat_in_alaska'), #5.5 #water-related-illnesses
            ('/metadata/figures/3734', 'projected_changes_in_caribbean_gambierdiscus_species'), #5.6 #water-related-illnesses
            ('/metadata/figures/3712', 'projections_of_growth_of_alexandrium_fundyense_in_puget_sound'), #5.7 #water-related-illnesses
        ]),
        ('food-safety--nutrition--and-distribution', [
            ('/metadata/figures/3579', 'farm_to_table'), #6.1 #food-safety--nutrition--and-distribution
            # ('/metadata/figures/3600', 'mycotoxin_in_corn'), #6.1 #food-safety--nutrition--and-distribution BOX 1?
            ('/metadata/figures/3809', 'climate_change_and_health__salmonella'), #6.2 #food-safety--nutrition--and-distribution
            ('/metadata/figures/3748', 'seasonality_of_human_illnesses_associated_with_foodborne_pathogens'), #6.3 #food-safety--nutrition--and-distribution
            ('/metadata/figures/3688', 'effects_of_carbon_dioxide_on_protein_and_minerals'), #6.4 #food-safety--nutrition--and-distribution
            ('/metadata/figures/3597', 'mississippi_river_level_at_st__louis__missouri'), #6.5 #food-safety--nutrition--and-distribution
        ]),
        ('extreme-weather', [
            ('/metadata/figures/3810', 'estimated_deaths_and_billion_dollar_losses_from_extreme_weather_events_in_the_u_s__2004_2013'), #7.1 #extreme-weather
            # ('/metadata/figures/3772', 'trends_in_flood_magnitude'), #7.2 #extreme-weather NOT USED
            ('/metadata/figures/3808', 'climate_change_and_health__flooding'), #7.2 #extreme-weather
            ('/metadata/figures/3760', 'hurricane_induced_flood_effects_in_eastern_and_central_united_states'), #7.3 #extreme-weather
        ]),
        ('mental-health-and-well-being', [
            ('/metadata/figures/3789', 'climate_change_and_mental_health'), #8.1 #mental-health-and-well-being
            ('/metadata/figures/3722', 'the_impact_of_climate_change_on_physical__mental__and_community_health'), #8.2 #mental-health-and-well-being
        ]),
        ('populations-of-concern', [
            ('/metadata/figures/3696', 'determinants_of_vulnerability'), #9.1 #populations-of-concern
            ('/metadata/figures/3694', 'social_determinants_of_health'), #9.2 #populations-of-concern
            ('/metadata/figures/3758', 'children_at_different_lifestages_experience_unique_vulnerabilities_to_climate_change'), #9.3 #populations-of-concern
            ('/metadata/figures/3714', 'mapping_social_vulnerability'), #9.4 #populations-of-concern
            ('/metadata/figures/3717', 'mapping_communities_vulnerable_to_heat_in_georgia'), #9.5 #populations-of-concern
        ]),
        ('appendix-1--technical-support-document', [
            ('/metadata/figures/3623', 'emissions_levels_determine_temperature_rises'), #1.1 #climate-change-and-human-health
            ('/metadata/figures/3759', 'the_shared_socioeconomic_pathways'), #1.2 #climate-change-and-human-health
            ('/metadata/figures/3726', 'example_spatial_resolution_of_climate_models'), #1.3 #climate-change-and-human-health
            ('/metadata/figures/3638', 'sensitivity_analysis_of_differences_in_modeling_approaches'), #1.4 #climate-change-and-human-health
        ])
    ])
}


def main():
    regenerate_image_id_map()
    image_id_map = pickle.load(open('image_id_cache.pk1', 'r'))

    for report_id in sync_metadata_tree:
        for chapter_id in sync_metadata_tree[report_id]:
            for survey_url, figure_id in sync_metadata_tree[report_id][chapter_id]:
                print survey_url

                s = surveys.get_survey(survey_url, do_download=False)

                # realize_parents(gcis, s.parents)
                # realize_contributors(gcis, s.contributors)

                for i in s.images:
                    i.identifier = image_id_map[i.identifier]
                    i.datasets = []
                    print gcis.create_image(i, report_id=report_id, figure_id=figure_id)


def regenerate_image_id_map(existing=None):
    from uuid import uuid4
    image_id_map = existing if existing else {}

    for report_id in sync_metadata_tree:
        for chapter_id in sync_metadata_tree[report_id]:
            for survey_url, figure_id in sync_metadata_tree[report_id][chapter_id]:
                s = surveys.get_survey(survey_url, do_download=False)
                for img in s.images:
                    if img.identifier in image_id_map:
                        print 'skipping: ', img.identifier
                        continue
                    else:
                        print 'added: ', img.identifier
                        image_id_map[img.identifier] = str(uuid4())

    with open('image_id_cache.pk1', 'wb') as fout:
        pickle.dump(image_id_map, fout)
    print 'image_id_map regenerated'


def gen_survey_list():
    realized_list = []
    chapters = [c for c in sync_metadata_tree['usgcrp-climate-and-health-assessment-draft']]

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
    hr = Report({})
    hr.identifier = 'usgcrp-climate-and-health-assessment-draft'
    hr.report_type_identifier = 'assessment'
    hr.title = 'Impacts of Climate Change on Human Health in the United States: A Scientific Assessment'
    hr.url = 'http://www.globalchange.gov/health-assessment'
    hr.publication_year = '2015'
    hr.contact_email = 'healthreport@usgcrp.gov'

    # ['report_identifier', 'identifier', 'number', 'title', 'url']
    chapters = [
        ('executive-summary', None, 'Executive Summary'),
        ('climate-change-and-human-health', 1, 'Climate Change and Human Health'),
        ('temperature-related-death-and-illness', 2, 'Temperature-Related Death and Illness'),
        ('air-quality-impacts', 3, 'Air Quality Impacts '),
        ('vectorborne-diseases', 4, 'Vectorborne Diseases'),
        ('water-related-illnesses', 5, 'Climate Impacts on Water-Related Illnesses'),
        ('food-safety--nutrition--and-distribution', 6, 'Food Safety, Nutrition, and Distribution'),
        ('extreme-weather', 7, 'Impacts of Extreme Events on Human Health'),
        ('mental-health-and-well-being', 8, 'Mental Health and Well-Being'),
        ('populations-of-concern', 9, 'Climate-Health Risk Factors and Populations of Concern'),
        ('appendix-1--technical-support-document', None, 'Appendix 1: Technical Support Document')
    ]

    # print gcis.create_report(hr)

    for id, num, title in chapters:
        ch = Chapter({})
        ch.identifier = id
        ch.number = num
        ch.title = title
        ch.report_identifier = hr.identifier

        print gcis.create_chapter(hr.identifier, ch)

main()