PR_USECOL = ['PRSN', 'APPL_CAT', 'APPL',
             'POS', 'TYPE', 'IS_7-1',
             'EA', 'LA', 'TC', 'SDC', 
             'QTY', 'ERT', 'DEPS',
             'ADDR', 'BLDG_ADMIN', 'BLDG_OWNER',
             'ATTR_1', 'ATTR_2', 'ATTR_3',
             'GR', 'IB_TYPE', 'IB_CAT', 
             'STAT', 'RESULT',
             'FR_DT', 'WD_DT', 'RJ_DT', 'PM_DT',
             'PN', 'C_PRCL'] #C_PRCL will be removed after get_district()

PR_RENAMED = ['PRSN', 'applicantCategory', 'applicantName', 
              'position', 'type', 'is_7_1', 
              'equipmentArea', 'landArea', 'totalCapacity', 'singleDeviceCapacity', 
              'quantity', 'retailing', 'dependencyType',
              'address', 'buildingAdmins', 'buildingOwners',
              'attribute_1', 'attribute_2', 'attribute_3',
              'isGreenRoof', 'illegalBuilding', 'illegalBuildingCategory',
              'status', 'result',
              'initialReceiveDate', 'withdrawDate', 'rejectionDate', 'permitDate',
              'georeferencedParcels', 'districtName'] #! districtName = relevantSection => for united purposes

ER_USECOL = ['同意備案編號','設備登記編號','設備面積_m2_', '土地面積_m2_', '總裝置容量_kW_', '單一裝置容量_kW_', '設備數量']
ER_RENAMED = ['PRSN', 'ERSN', 'equipmentArea_ER', 'landArea_ER', 'totalCapacity_ER', 'singleDeviceCapacity_ER', 'quantity_ER']

PRCL_USECOL = ["PN", "TNAME", "SECNAME", "SECT", "LANDNO8", "LAND_NO", 
               "AREA", "AA11", "AA12", "AA08", "AA16", "AA17",
               "BBType", "BB09", "Mng", "LONG", "LAT"]
PRCL_RENAMED =["_id", "districtName", "sectionName", "prefix", "prcl8", "prcl",
               "area", "landUseZoning", "landUseType", "landCategory", "presentValue", "landValue",
               "ownershipType", "owner", "admin", 'longitude', 'latitude']

LS_USECOL = ["APPL", "SESS", "C_AREA", "CAP", "STAT", "PN",
             "ALUC_DT", "EA_DT", "LCC_DT", "LCR_DT", 
             "AJOC", "BLDG", "NBR", "ESA", "INR", "EXPLICIT"]
LS_RENAMED = ["name", "session", "caseArea", "capacity", "status", "parcels",
              "agriLandUseChangeDate", "establishmentApprovalDate", "landUseChangeDate", "landUseChangeRegisDate",
              "isAdjacent", "isBuilding", "isNearbyResident", "isSensitive", "isInner", "isExplicit"]
