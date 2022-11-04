import env


def wrangle_single_family_residential():
    ''' Wrangle_single_family_residential imports data Zillow properties_2017 from codeup database
        using an sql querry and env file and drops all nan values.
        Returns cleaned data frame
    '''
   
    # squl query for acquisition
    sql_query = """
                SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
                FROM properties_2017
                Where propertylandusetypeid = 261;
                """
    # Acquisition
    df = pd.read_sql(sql_query, env.get_connection('zillow'))
    
    df = df.dropna()
    

    return df