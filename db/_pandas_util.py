
import os
import pandas as pd
import numpy as np
from typing import Literal
from db._db_usecol import *

def reip_readfile(path: str,
                   mode: Literal['pr', 'er', 'ls', 'parcel']) -> pd.DataFrame:
    '''
    `PR, LS` should be georeferenced,
    `ER` should be raw data,
    `parcel` does not matter. ( every georeferenced data has the same fields since it's originally joined by attribute. )
    '''
    match mode:
        case 'pr':
            df = (
                _pandas_readfile(path)[PR_USECOL]
                .set_axis(PR_RENAMED, axis=1)
                .fillna(np.nan)
            )
            
        case 'er':
            df = (
                _pandas_readfile(path)[ER_USECOL]
                .set_axis(ER_RENAMED, axis=1)
            )
        case 'ls':
            df = (
                _pandas_readfile(path)[LS_USECOL]
                .set_axis(LS_RENAMED, axis=1)
                .fillna(np.nan)
            )
        case 'parcel':
            df = (
                _pandas_readfile(path)[PRCL_USECOL]
                .set_axis(PRCL_RENAMED, axis=1)
                .fillna(np.nan)
                .drop_duplicates()
                .astype({"_id": "str",
                         "prefix": "str",
                         "prcl8": "str",
                         "prcl": "str",
                         "landCategory": "category",
                         "landUseZoning": "category",
                         "landUseType": "category",})
            )
    
    return df


def _pandas_readfile(path):
    USE_FUNC = {
        '.csv': pd.read_csv,
        '.xlsx': pd.read_excel,
        '.xls': pd.read_excel
    }
    ftype = os.path.splitext(path)[1].lower()
    return USE_FUNC[ftype](path)

