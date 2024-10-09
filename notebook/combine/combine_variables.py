from demographics.demographics_results import 'gender_output.csv', 'race_output.csv', 'weight_output.csv', 'height_output.csv'
from lab.lab_results import *
from vitalsigns.vitalsigns_results import *
from comorbidity.comorbidity_results import *
from utils.utils import reindex

sorted_data_path = '/media/data/huyennm/mimic-iv/notebook/combine/sorted_data'


reindex(gender_output.csv, os.path.join(sorted_data_path, 'gender_output.csv'))
