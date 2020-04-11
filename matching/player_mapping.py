import pandas as pd
import numpy as np
from fuzzywuzzy import process

mock = pd.read_excel('C:/Users/rdtay/documents/wagering/nfl/draft/mock_full.xlsx')
master = list(mock[mock['AUTHOR']=='walter-football']['PLAYER'])
authors = list(pd.unique(mock['AUTHOR']))
sites = list(pd.unique(mock['SITE']))
master_df = pd.DataFrame(data = {'MASTER': master})
match_df = master_df.merge(right = mock[mock['SITE']=='nfl.com']['PLAYER'], how = 'left', left_on = 'MASTER', right_on = 'PLAYER').merge(
        right = mock[mock['SITE']=='cbs.com']['PLAYER'], how = 'left', left_on = 'MASTER', right_on = 'PLAYER').merge(right = 
                    mock[mock['SITE']=='sbnation']['PLAYER'], how = 'left', left_on = 'MASTER', right_on = 'PLAYER').drop_duplicates().rename(
                            columns = {'PLAYER_x':'NFL', 'PLAYER_y':'CBS', 'PLAYER':'SBNATION'})


sites = ['nfl.com', 'cbs.com', 'sbnation']

for j in range(1, len(sites)+1):            
    for i in range(0, len(match_df['MASTER'])):
        if match_df.iloc[i][j] is np.nan:
            if process.extractOne(match_df.iloc[i][0], list(mock[mock['SITE']==sites[j - 1]]['PLAYER']))[1] >= 90:
                match_df.iloc[[i],[j]] = process.extractOne(match_df.iloc[i][0], list(mock[mock['SITE']==sites[j - 1]]['PLAYER']))[0]
                print(match_df.iloc[i][0] + ' matched with ' + process.extractOne(match_df.iloc[i][0], list(mock[mock['SITE']==sites[j - 1]]['PLAYER']))[0]
                + ' accuracy: ' + str(process.extractOne(match_df.iloc[i][0], list(mock[mock['SITE']==sites[j - 1]]['PLAYER']))[1]))
        
    
