import env
import os
import numpy as np
import pandas as pd

def get_zillow_data():
        ''' Acquire Zillow data using properties_2017 table from Code up Data Base. Columns bedroomcnt, 
            bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips 
        '''
   
         # sql query for acquisition
        sql_query = """
        SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
        FROM properties_2017
        Where propertylandusetypeid = 261;
        """
        # Acquisition
        df = pd.read_sql(sql_query, env.get_connection('zillow'))
        return df



def wrangle_single_family_residential():
    '''Wrangle_single_family_residential checks to see if the csv or zillow data exits. If it does not
        it will call for the data and save a csv file. It will return a dataframe that had drop all nulls.
    '''
    # obtain csv file
    if os.path.isfile('zillow.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('zillow.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = get_zillow_data()
        
        # Cache data
        df.to_csv('zillow.csv')
    # replace blank spaces and special characters
    df = df.replace(r'^\s*$', np.nan, regex = True)
   
    # drop nan
    df = df.dropna()

    # rename columns
    df = df.rename(columns={'bedroomcnt': 'bedroom','bathroomcnt': 'bathroom',
            'calculatedfinishedsquarefeet': 'squarefeet','taxvaluedollarcnt': 'tax_value'})
    return df



def scale_data(train, 
               validate, 
               test, 
               columns_to_scale=['bedroom', 'bathroom', 'squarefeet', 'taxamount']):
    '''
    scale_data takes in train , validate, test data  and returns their scaled counterparts.
    '''
    # create copies of our original data
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    #create the scaler
    scaler = QuantileTransformer(output_distribution='normal')
    # fit the scaler into train data
    scaler.fit(train[columns_to_scale])
    
    # applying the scaler to train, validate, and test data
    train_scaled[columns_to_scale] = pd.DataFrame(scaler.transform(train[columns_to_scale]),
                                                  columns=train[columns_to_scale].columns.values).set_index([train.index.values])
                                                  
    validate_scaled[columns_to_scale] = pd.DataFrame(scaler.transform(validate[columns_to_scale]),
                                                  columns=validate[columns_to_scale].columns.values).set_index([validate.index.values])
    
    test_scaled[columns_to_scale] = pd.DataFrame(scaler.transform(test[columns_to_scale]),
                                                 columns=test[columns_to_scale].columns.values).set_index([test.index.values])
    
    return train_scaled, validate_scaled, test_scaled