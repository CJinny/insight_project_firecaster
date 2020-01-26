
import pandas as pd
import subprocess
import glob
#c = pd.read_csv('bigquery_results.csv')
c = pd.read_csv('bigquery_results_s.csv')

G = [*map(lambda t:t.split('/')[-1], glob.glob('/Volumes/My Passport for Mac/sentinel_2_53HPA/S2*'))]


for i in c['base_url']:
    if i.split('/')[-1] not in G:
        #print(i)
        subprocess.run(f"gsutil cp -r {i} .", shell=True, check=True)
