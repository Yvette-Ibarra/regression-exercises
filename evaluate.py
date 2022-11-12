import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


####################################### PLOT RESIDUALS #############################################
def plot_residuals(y, yhat):
    '''
    plot_residuals takis in acutal value of target y and predicted value and returns a scatter plot of reiduals.
    y: targets acutal value
    yhat: predicted value or target
    '''
    # calculate residauals
    residuals = y - yhat
    
    # create scatter plot
    plt.scatter(x=y, y=residuals)

    # create labels for axis and title
    plt.xlabel('Home Value')
    plt.ylabel('Residuals')
    plt.title('Residual vs Home Value Plot')

    # show plot
    plt.show()


################################################ REGRESSION ERRORS #################################
def regression_errors(y, yhat):
    '''
    regression_errors takes in actual value  of target y  and predicted value yhat 
    and returns  SSE, ESS, TSS, MSE, RMSE
    y: actual values of target
    yhat: predicted value of target
    
    Return :
        * SSE Sum or Squared error
        * ESS Explained sum of squares
        * TSS Total sum of squares
        * MSE Mean squared error
        * RMSE Root mean squared error
        
    '''

    # calculations
    MSE = mean_squared_error(y, yhat)
    SSE = MSE * len(y)
    RMSE = MSE**.5
    ESS = ((yhat - y.mean())**2).sum()
    TSS = ESS + SSE
    
    return f'SSE = {SSE}', f'ESS = {ESS}', f'TSS = {TSS}', f'MSE = {MSE}', f'RMSE = {RMSE}'


######################################### BASELINE MEAN ERORS ############################################
def baseline_mean_errors(y):
    '''
    baseline mean errors takes in acutal target and returns baseline: SSE, MSE, RMSE
    y: actual target values

    Returns:
        * SSE: baseline sum of squared error
        * MSE: baseline mean square error
        * RMSE: baseline root mean square error
    '''
    # set baseline
    baseline = np.repeat(y.mean(), len(y))
    # calculations
    MSE = mean_squared_error(y, baseline)
    SSE = MSE * len(y)
    RMSE = MSE**.5
    
    return f'baseline SSE = {SSE}',f'baseline MSE = {MSE}', f'baseline RMSE = {RMSE}'

######################################## BETTER THAN BASELINE ########################################
def better_than_baseline(y, yhat):
  
     # calculations
    MSE = mean_squared_error(y, yhat)
    SSE = MSE * len(y)
    RMSE = MSE**.5
    ESS = ((yhat - y.mean())**2).sum()
    TSS = ESS + SSE
    
    
    # set baseline
    baseline = np.repeat(y.mean(), len(y))
    # calculations
    MSE = mean_squared_error(y, baseline)
    SSE = MSE * len(y)
    RMSE = MSE**.5

    # calculate diffirences
    SSE_baseline, MSE_baseline, RMSE_baseline = baseline_mean_errors(y)
    
    if SSE < SSE_baseline:
        print('My OSL model performs better than baseline')
    else:
        print('My OSL model performs worse than baseline. :( )')