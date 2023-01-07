
import pandas as pd


def reip_to_geojson(prcl_df: pd.DataFrame  #! _pandas_readfile(georeferenced_pr_file_path, 'parcel')
                    ) -> dict:
    parcel_data = list(_parcel_to_geojson(prcl_df))
    return parcel_data


def _parcel_to_geojson(df: pd.DataFrame) -> dict:
    names = df.columns[:-2]
    for _, row in df.iterrows():
        output = dict(zip(names, row[names]))
        output['location'] = {"type":"Point", 
                              "coordinates":[row.longitude, row.latitude]}
        yield output
        
