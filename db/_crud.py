
import pymongo
import numpy as np
import pandas as pd
import datetime as dt


def create_parcel_collection(df: pd.DataFrame, collection: pymongo.collection.Collection):
    # df = pd.read_excel("/Users/cookie/Desktop/ls20221220_tmp.xlsx")
    df.fillna(np.nan)
    df = df[["PN", "TNAME", "SECNAME", "SECT", "LANDNO8", "LAND_NO", 
            "AREA", "AA11", "AA12", "AA08", "AA16", "AA17",
            "BBType", "BB09", "Mng"]]
    df.columns = ["_id", "districtName", "sectionName", "prefix", "prcl8", "prcl",
                "area", "landUseZoning", "landUseType", "landCategory", "presentValue", "landValue",
                "ownershipType", "owner", "admin"]
    df = df.drop_duplicates()
    df = df.astype({
        "_id": "str",
        "prefix": "str",
        "prcl8": "str",
        "prcl": "str",
        "landCategory": "category",
        "landUseZoning": "category",
        "landUseType": "category",
        })
    parcel_data = df.to_dict("records")
    collection.insert_many(parcel_data)


def create_applicants_collection(df: pd.DataFrame, collection: pymongo.collection.Collection):
    # df = pd.read_excel("/Users/cookie/Desktop/ls20221220_tmp.xlsx")
    df.fillna(np.nan)

    df = df[["APPL", "SESS", "C_AREA", "CAP", "STAT", "PN",
            "ALUC_DT", "EA_DT", "LCC_DT", "LCR_DT", 
            "AJOC", "BLDG", "NBR", "ESA", "INR", "EXPLICIT"]]
    df.columns = ["name", "session", "caseArea", "capacity", "status", "parcels",
                "agriLandUseChangeDate", "establishmentApprovalDate", "landUseChangeDate", "landUseChangeRegisDate",
                "isAdjacent", "isBuilding", "isNearbyResident", "isSensitive", "isInner", "isExplicit"]

    def is_true(s):
        try:    return "X" in s.lower()
        except: return True

    def correct_dt(s):
        if not s: return pd.NaT
        try:
            s = str(s)
            y,m,d = map(int, map(float, [s[:3], s[3:5], s[5:]]))
            y = y + 1911
        except:
            return pd.NaT
        
        return dt.datetime.strptime(f"{y}-{m}-{d}", "%Y-%m-%d")

    df.agriLandUseChangeDate = df.agriLandUseChangeDate.apply(correct_dt)
    df.establishmentApprovalDate = df.establishmentApprovalDate.apply(correct_dt)
    df.landUseChangeDate = df.landUseChangeDate.apply(correct_dt)
    df.landUseChangeRegisDate = df.landUseChangeRegisDate.apply(correct_dt)
    df[["isAdjacent", "isBuilding", "isNearbyResident", "isSensitive", "isInner", "isExplicit"]] =\
        df[["isAdjacent", "isBuilding", "isNearbyResident", "isSensitive", "isInner", "isExplicit"]].apply(is_true)
    df.status = df.status.astype("category")

    gf = df.groupby(["name", "session", "caseArea"]).agg( lambda x: ",".join(map(str, list(set(x)))) ).reset_index()
    gf.parcels = gf.parcels.apply(lambda x : x.split(","))
    appl_data = gf.to_dict("records")
    collection.insert_many(appl_data)



# * connect to db
# client = _connect_mongo()
# ls = client.ls
# * create collection
# parcel = ls.parcel
# applicant = ls.applicant
# * insert data
# create_parcel_collection(parcel)
# create_applicants_collection(applicant)
