
import pandas as pd
import datetime as dt
from db._db_usecol import *

#? <-----  Create json data ----->
def ls_to_json(ls_df: pd.DataFrame,
               sep=','
               ) -> dict:
    '''
    frrom _pandas_util import reip_read_file
    ----------------------------------
    ls_df = reip_read_file(patj, 'ls')
    '''
    ls_df = _modify_ls_df(ls_df)
    gf =  (
        ls_df
        .groupby(["name", "session", "caseArea"])
        .agg( lambda x: sep.join(map(str, list(set(x)))) )
        .reset_index()
        )
    
    gf.parcels = gf.parcels.apply(lambda x : x.split(","))
    
    return gf.to_dict('records')


#? <----- sub functions ----->
def _ls_to_bool(s: pd.Series):
    try:    
        return "X" in s.lower()
    except: 
        return True
    
    
def _ls_roc_to_dt(s: pd.Series):
    if not s: 
        return pd.NaT
    try:
        s = str(s)
        y,m,d = map(int, map(float, [s[:3], s[3:5], s[5:]]))
        y = y + 1911
    except:
        return pd.NaT
    
    return dt.datetime.strptime(f"{y}-{m}-{d}", "%Y-%m-%d")


def _modify_ls_df(df: pd.DataFrame) -> pd.DataFrame:
    '''
    correct dtypes of LS DataFrame
    '''
    ## datetime
    df.agriLandUseChangeDate = df.agriLandUseChangeDate.apply(_ls_roc_to_dt)
    df.establishmentApprovalDate = df.establishmentApprovalDate.apply(_ls_roc_to_dt)
    df.landUseChangeDate = df.landUseChangeDate.apply(_ls_roc_to_dt)
    df.landUseChangeRegisDate = df.landUseChangeRegisDate.apply(_ls_roc_to_dt)
    ## boolean
    df[["isAdjacent", "isBuilding", "isNearbyResident", "isSensitive", "isInner", "isExplicit"]] =\
        df[["isAdjacent", "isBuilding", "isNearbyResident", "isSensitive", "isInner", "isExplicit"]].apply(_ls_to_bool)
    ## category
    df.status = df.status.astype("category")
    
    return df
    
