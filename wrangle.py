import env

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
    
    df = df.dropna()
    return df