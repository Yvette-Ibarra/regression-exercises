import env
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import QuantileTransformer

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


def remove_outliers(df,feature_list):
    ''' utilizes IQR to remove data which lies beyond 
    three standard deviations of the mean
    '''
    for feature in feature_list:
    
        #define interquartile range
        Q1= df[feature].quantile(0.25)
        Q3 = df[feature].quantile(0.75)
        IQR = Q3 - Q1
        #Set limits
        upper_limit = Q3 + 3 * IQR
        lower_limit = Q1 - 2.5 * IQR

        #remove outliers
        df = df[(df[feature] > lower_limit) & (df[feature] < upper_limit)]
    
    return df

def handle_outliers(df):
    """Manually handle outliers that do not represent properties likely for 99% of buyers and zillow visitors"""
    df = df[df.bathroom <= 8]
    
    df = df[df.bedroom<= 8]

    df = df[df.tax_value < 2_000_000]

    df = df[df.squarefeet < 10000]

    return df


def split_data(df):
    '''
    split_data takes in data Frame and splits into  train , validate, test.
    The split is 20% test 80% train/validate. Then 30% of 80% validate and 70% of 80% train.
    Aproximately (train 56%, validate 24%, test 20%)
    Returns train, validate, and test 
    '''
    # split test data from train/validate
    train_and_validate, test = train_test_split(df, random_state=123, test_size=.2)

    # split train from validate
    train, validate = train_test_split(train_and_validate, random_state=123, test_size=.3)
                                   
    return train, validate, test

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