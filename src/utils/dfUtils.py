import pandas

from utils.converterutils import addHeader


def mergeDF(left, right):   
    return pandas.merge(left, right,how='outer', on='ds') 
        
        
        
def mergeColumnmap(leftColumnmap, rightColumnmap, mergedColumnlist):  
    columnmap={}
    count =1
    for key, value in leftColumnmap.items():
        if key == 'ds':
            continue
        columnmap[mergedColumnlist[count]]= value
        count +=1     
    for key, value in rightColumnmap.items():
        if key == 'ds':
            continue
        columnmap[mergedColumnlist[count]]= value
        count +=1  
    return columnmap



# dataframe summary. Can be used on notebook
def dataSummary(df):
    for column in df.columns:
        print(column)
        if df.dtypes[column] == np.object: # Categorical data
            print(df[column].value_counts())
        else:
            print(df[column].describe())
        print('\n')




def getStartTime(dataframe, hasIndex = True):
    if hasIndex:
        return dataframe.index[0]
    return dataframe.ds[0] 


def getLastTime(dataframe, hasIndex = True):
    size = dataframe.shape[0]
    if hasIndex:
        return dataframe.index[size-1]
    return dataframe.ds[size-1] 

def dataframe_substract(df1,df2,time_diff=86400):
    newdf1= addHeader(df1.index+time_diff, df1.y.values)
    df = newdf1.merge(df2, how='inner' , left_index=True, right_index=True)
    df['y']=df.apply(lambda row: row.y_x-row.y_y, axis=1)
    return df



def ts_filter(dataframe, lower, higher=None, isGreatThan=True, hasIndex=True):
  if higher is None:
    if hasIndex == True:
        if isGreatThan:
             return dataframe[dataframe.index > lower]
        return dataframe[dataframe.index <= lower]
    if isGreatThan:
        return dataframe[dataframe.y > lower]
    return dataframe[dataframe.y <= lower]
  else: 
    if lower > higher:
        tmp = lower
        lower = higher
        higher = tmp
    if hasIndex == True:
        df1=dataframe[dataframe.index > lower]
        df2=df1[df1.index <= higher]
        return df2
    df1 =dataframe[dataframe.y > lower]
    df2 = df2[df1.y <= higher]