def expand_nbr(name='L1C_T53HPA_A004418_20180110T005319', 
                 BASE = '/Volumes/My Passport for Mac/sentinel_2_53HPA/',
                 #OUT='/Volumes/My Passport for Mac/'
                A=100
                 ):
    
    ## add 200 paddings outwards!
    smooth=1e-5
    b08 = rasterio.open(BASE+name+'_b08.tif').read(1)
    b08 = np.expand_dims(cv2.resize(b08, (5490,5490)), axis=2)[3000-A:4000+A,2200-A:3200+A,:]
    b12 = np.expand_dims(rasterio.open(BASE+name+'_b12.tif').read(1), axis=2)[3000-A:4000+A,2200-A:3200+A,:]
    nbr = (b08-b12+smooth)/(b08+b12+smooth)
    nbr = np.expand_dims(nbr, 0)
    return nbr


bigquery_res = pd.read_csv('/Volumes/My Passport for Mac/sentinel_2_53HPA/bigquery_results_s.csv', index_col=0)
bigquery_res['sensing_time'] = pd.to_datetime(bigquery_res['sensing_time'])
bigquery_res = bigquery_res[bigquery_res['cloud_cover']<75]
bigquery_res = bigquery_res.reset_index(drop=True)

dnbr_s = dnbr[:,200:1200,100:1100,:]
dnbr_n = dnbr[:,0:1000,100:1100,:]
dnbr_w = dnbr[:,100:1100,0:1000,:]
dnbr_e = dnbr[:,100:1100,200:1200,:]

dnbr_nw = dnbr[:,0:1000,0:1000,:]
dnbr_sw = dnbr[:,200:1200,0:1000,:]
dnbr_ne = dnbr[:,0:1000,200:1200,:]
dnbr_se = dnbr[:,200:1200,200:1200,:]

dnbr_list  = [dnbr_s, dnbr_n, dnbr_w, dnbr_e, dnbr_nw, dnbr_sw, dnbr_ne, dnbr_se]
suffix_list= ['south','north','west','east','northwest','southwest','northeast','southeast']


for name in bigquery_res_s['granule_id'].values:
    if name=='L1C_T53HPA_A004418_20180110T005319':
        nbr = expand_nbr(name=name)
    else:
        nbr = np.concatenate([nbr, expand_nbr(name=name)],0)
    
dnbr = np.zeros((108,1200,1200,1))
for i in range(108):
    dnbr[i,:] = nbr[i+1,:] - nbr[i,:]

np.savez_compressed('adjacency', dnbr=dnbr)

def generate_adjacency_feature(dnbr_list, suffix_list):
    trn_adjacency = pd.DataFrame()
    val_adjacency = pd.DataFrame()
    for I in range(5):
        trn_idx = [i for i in range(25) if i not in range(5*I, 5*I+5)]
        val_idx = [i for i in range(25) if i in range(5*I, 5*I+5)]
    
        for i in range(len(dnbr_list)):
            trn_y = generate_sectos_combined((dnbr_list[i]>=0.66).astype(int), indices=trn_idx)
            val_y = generate_sectos_combined((dnbr_list[i]>=0.66).astype(int), indices=val_idx)
            trn_y_0, trn_y_1, trn_y_2 = iterate_data(trn_y, size=108)
            val_y_0, val_y_1, val_y_2 = iterate_data(val_y, size=108)

            trn_adjacency[f'f_{I}_s_0_d_{suffix_list[i]}'] = trn_y_0
            trn_adjacency[f'f_{I}_s_1_d_{suffix_list[i]}'] = trn_y_1
            trn_adjacency[f'f_{I}_s_2_d_{suffix_list[i]}'] = trn_y_2
            val_adjacency[f'f_{I}_s_0_d_{suffix_list[i]}'] = val_y_0
            val_adjacency[f'f_{I}_s_1_d_{suffix_list[i]}'] = val_y_1
            val_adjacency[f'f_{I}_s_2_d_{suffix_list[i]}'] = val_y_2
    return trn_adjacency, val_adjacency       
            
trn_adjacency, val_adjacency = generate_adjacency_feature(dnbr_list, suffix_list)
trn_adjacency.to_csv('trn_adjacency.csv', index=False)
val_adjacency.to_csv('val_adjacency.csv', index=False)
