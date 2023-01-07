
import pandas as pd
import numpy as np


#? <-----  Create json data ----->
def reip_to_json(pr_df: pd.DataFrame,   #! _pandas_readfile(georeferenced_pr_file_path, 'data')
                 er_df: pd.DataFrame,   #! _pandas_readfile(rawdata_er_file_path)
                 sep = ','              # doesn't really matter, ensure both situations are the same
                 ) -> dict:
    '''
    frrom _pandas_util import reip_read_file
    ----------------------------------
    pr_df = reip_read_file(patj, 'pr')
    er_df = reip_read_file(patj, 'er')
    '''
    
    gf = (
        pr_df
        .groupby(["PRSN"])
        .agg( lambda x: sep.join(map(str, list(set(x)))) )
        .reset_index()
        )
    
    
    #? moditfy georeferencedParcels from "string" to "array"
    #? "str(PN), str(PN), ..." ->  [str(PN), str(PN), ...]
    gf.georeferencedParcels = gf.georeferencedParcels.apply(lambda x : x.split(sep))
    #? reset dtypes
    gf = _modify_pr_df(gf)
   
    #? merge ER into PR: 
    #? assert all ER's PRSN are within PR's PRSN
    merged = gf.merge(er_df, 
                      on='PRSN', 
                      how='left')    #! merged based on PR DataFrame
    
    return merged.to_dict('records')


#? <----- sub functions ----->
def _modify_pr_df(df: pd.DataFrame) -> pd.DataFrame:
    '''
    reset dtypes of the PR DataFrame
    '''
    ## float
    df.landArea = df.landArea.apply(_reip_to_float)
    df.totalCapacity = df.totalCapacity.apply(_reip_to_float)
    df.equipmentArea = df.equipmentArea.apply(_reip_to_float)
    ## datetime
    df.initialReceiveDate = pd.to_datetime(df.initialReceiveDate, errors='coerce')
    df.withdrawDate = pd.to_datetime(df.withdrawDate, errors='coerce')
    df.rejectionDate = pd.to_datetime(df.rejectionDate, errors='coerce')
    df.permitDate = pd.to_datetime(df.permitDate, errors='coerce')
    #! fix NaT values
    df.initialReceiveDate = df.initialReceiveDate.astype(object).where(df.initialReceiveDate.notnull(), None)
    df.withdrawDate = df.withdrawDate.astype(object).where(df.withdrawDate.notnull(), None)
    df.rejectionDate = df.rejectionDate.astype(object).where(df.rejectionDate.notnull(), None)
    df.permitDate = df.permitDate.astype(object).where(df.permitDate.notnull(), None)
    ## category
    df.status = df.status.astype("category")
    df.result = df.result.astype("category")
    df.position = df.position.astype("category")
    df.type = df.type.astype("category")
    df.applicantCategory = df.applicantCategory.astype("category")
    df.illegalBuilding = df.illegalBuilding.astype("category")
    df.illegalBuildingCategory = df.illegalBuildingCategory.astype("category")
    ## boolean
    df.is_7_1 = df.is_7_1.apply(_reip_to_bool)
    df.retailing = df.retailing.apply(_reip_to_bool)
    df.isGreenRoof = df.isGreenRoof.apply(_reip_to_bool)
    
    return df
    

def _reip_to_bool(s: pd.Series):
    try:    
        return bool(False * ("否" in s.lower() or '無' in s.lower() or np.isnan(s)))
    except: 
        return True


def _reip_to_float(s: pd.Series):
    try:
        return float(s)
    except:
        return float(0)

    