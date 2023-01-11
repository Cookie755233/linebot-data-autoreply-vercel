
import os
import re
import pandas as pd
import numpy as np
from typing import Literal
from const.db import *
from collections import defaultdict


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
                .assign(relevantSection = lambda s: _get_district(s, parcel_colname='C_PRCL'))
                .drop(columns=['C_PRCL'])
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


def _get_district(df, parcel_colname: str) -> list:
    '''
    !! << 不要放入依地號分割後的DataFrame >>

    以「案號」為單位，找出各案場位於哪個行政區
    出現複數行政區案場以最多的為主。 
-> ['行政區', ...]: list
    '''
    ### Sub-functions ###
    def formatted_count():
        district = []

        for _, series in df.iterrows():
            tmp = defaultdict(int)
            parcel = series[parcel_colname]
            if not pd.isna(parcel):
                for p in parcel.split(','):
                    try:
                        _, D = re.findall(r'(.*?市)?(.*?區)', p)[0]
                        tmp[D] += 1
                    except IndexError:
                        continue
                if tmp:
                    district.append(max(tmp, key=tmp.get))
                else:
                    district.append('')
            else:
                district.append('')

        return district


    ### Main ###
    DISTRICT = formatted_count()

    # df['行政區'] = DISTRICT
    return DISTRICT