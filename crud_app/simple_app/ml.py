import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
# %matplotlib inline
from statsmodels.tsa.stattools import adfuller
from pandas.plotting import autocorrelation_plot
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from pandas.tseries.offsets import DateOffset
from statsmodels.tsa.arima.model import ARIMA


# import os 
# import cv2

# from pmdarima import auto_arima 
# from sklearn.metrics import mean_squared_error
# from statsmodels.tools.eval_measures import rmse

def process(df):
    # df.columns=["Month","Sales"]
    # df.drop(106,axis=0,inplace=True)
    # df.drop(105,axis=0,inplace=True)
    df['Date']=df['Year'].astype(str)+"-"+df['Month'].astype(str)
    df=df[["Date","Quantity"]]
    df['Date']
    df.rename(columns={"Date":"Month","Quantity":"Sales"},inplace=True)
    # Convert Month into Datetime
    df['Month']=pd.to_datetime(df['Month'])

    df.set_index('Month',inplace=True)

    ### Testing For Stationarity
    test_result=adfuller(df['Sales'])

    #Ho: It is non stationary
    #H1: It is stationary

    commentlist=[]
    def adfuller_test(sales,char):
        result=adfuller(sales)
        commentdict={}
        commentdict['Name']=char
        labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']
        for value,label in zip(result,labels):
            commentdict[label]=str(value)
            # print(label+' : '+str(value) )
        if result[1] <= 0.05:
            commentdict['Comment']="strong evidence against the null hypothesis(Ho), reject the null hypothesis. Data has no unit root and is stationary"
            # print("strong evidence against the null hypothesis(Ho), reject the null hypothesis. Data has no unit root and is stationary")
        else:
            commentdict['Comment']="weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary "
            # print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")
        commentlist.append(commentdict)
        
    adfuller_test(df['Sales'],'Sales')
    df['Sales First Difference'] = df['Sales'] - df['Sales'].shift(1)
    df['Sales'].shift(1)

    df['Seasonal First Difference']=df['Sales']-df['Sales'].shift(12)

    ## Again test dickey fuller test
    adfuller_test(df['Seasonal First Difference'].dropna(),"Seasonal First Difference")

    autocorrelation_plot(df['Sales'])

    # fig = plt.figure(figsize=(12,8))
    # ax1 = fig.add_subplot(211)
    # fig = sm.graphics.tsa.plot_acf(df['Seasonal First Difference'].iloc[13:],lags=40,ax=ax1)
    # ax2 = fig.add_subplot(212)
    # fig = sm.graphics.tsa.plot_pacf(df['Seasonal First Difference'].iloc[13:],lags=40,ax=ax2)

    #auto_arima test
    # stepwise_fit = auto_arima(df["Sales"], start_p = 1, start_q = 1,max_p = 3, max_q = 3, m = 12,start_P = 0, seasonal = True,d = None, D = 1, 
    #                         trace = True,error_action ='ignore',suppress_warnings = True, stepwise = True)

    #testing arima and rsme values

    # start=len(df['Sales'])
    # end=len(df['Sales'])*2-1
    # predictions = results.predict(start,end,typ='levels',dynamic=True)
    # display(rmse(df['Sales'],predictions))
    # display(mean_squared_error(df['Sales'],predictions))
        
    #arima and sarimax    
    model=ARIMA(df['Sales'],order=(1,1,1))
    model_fit=model.fit()

    # df['forecast']= model_fit.predict(start=90,end=103,dynamic=True)

    model=sm.tsa.statespace.SARIMAX(df['Sales'],order=(1, 1, 1),seasonal_order=(1,1,1,12))
    results=model.fit()

    future_dates=[df.index[-1]+ DateOffset(months=x) for x in range(0,24)]
    future_datest_df=pd.DataFrame(index=future_dates[1:],columns=df.columns)
    length=len(df.index)

    # future_df[['Sales','forecast']].plot(figsize=(12, 8))
    future_df=pd.concat([df,future_datest_df])
    future_df['forecast']=results.predict(start=length,end=length+24,dynamic=True)
    # future_df.plot()

    future_df['Dates']=future_df.index
    future_df.reset_index(drop=True)
    future_df=future_df[['Dates',"Sales","Sales First Difference","Seasonal First Difference",'forecast']]
    future_df.to_csv('changed.csv',index=False)

    #saving image file
    # def save_img(loca,x,y,z):
    #     x.plot(figsize=(28,7))

    #     imgp = os.path.join('static', y +'.png')
    #     plt.savefig(imgp)
    #     vartemp = "D:\Kaar rec\project\FRS\crud_app\static" + y + "\.png"
    #     # path = r'"D:\Kaar rec\project\FRS\crud_app\static" + y + "\.png"'
    #     dirt = r'D:\Kaar rec\project\FRS\angular\src\assets'

    #     img = cv2.imread(vartemp)
    #     os.chdir(dirt)
    #     filename =z
    #     cv2.imwrite(filename,img)

    # save_img(future_df,"image","sales.png")

    # #savefile static
    # future_df.plot(figsize=(28,7))
    # imgp = os.path.join('static',"image"+'.png')
    # plt.savefig(imgp)
    # path = r'D:\Kaar rec\project\FRS\crud_app\static\image.png'
    # dirt = r'D:\Kaar rec\project\FRS\angular\src\assets'
    # img = cv2.imread(path)
    # os.chdir(dirt)
    # filename = "sales2.png"
    # cv2.imwrite(filename,img)


    # temp=future_df.plot(figsize=(28,7))
    # fig=temp.get_figure()
    # fig.savefig('./angular/src/assets/output.png')

    
    #storing values in list
    z=[]
    for i in list(future_df.index):
        z.append(str(i).split()[0])
    x=list(future_df['Sales'].dropna())
    y=list(future_df['forecast'].dropna())


    return [z,x,y,commentlist]
