def create_bubble():
    return {
        "type": "bubble",
        "body": {"type": "box", "layout": "vertical", "contents": []},
        "styles": {"footer": {"separator": True}},
    }


def insert_body_contents_TITLE(bubble, 
                               top,     #? 上標（綠字/紅字）
                               title,   
                               appendix,
                               top_color="#46844f"
                               ):    
    bubble["body"]["contents"] += [
        {
            "type": "text",
            "text": top,
            "weight": "bold",
            "color": top_color,
            "size": "sm",
        },
        {
            "type": "text",
            "text": title,
            "weight": "bold",
            "size": "lg",
            "margin": "md",
            "wrap": True
        },
        {
            "type": "text",
            "text": appendix,
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
        },
    ]
    return bubble


def insert_body_contents_ITEM(bubble, 
                              subtitle,     #? subtitle
                              key_1, val_1, #? attribute 1
                              key_2, val_2, #? attribute 2
                              key_3, val_3, #? attribute 3
                              ):
    bubble["body"]["contents"] += [
        {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": subtitle,
                    "size": "md",
                    "weight": "bold",
                    "color": "#46844f",
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": key_1,
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": val_1,
                            "size": "sm",
                            "color": "#111111",
                            "align": "end",
                        },
                    ],
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": key_2,
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": val_2,
                            "size": "sm",
                            "color": "#111111",
                            "align": "end",
                        },
                    ],
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": key_3,
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": val_3,
                            "size": "sm",
                            "color": "#111111",
                            "align": "end",
                        },
                    ],
                },
            ],
        },
    ]
    return bubble


def insert_body_contents_FOOTER(bubble, 
                                key_1, val_1):
    bubble["body"]["contents"] += [
        {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
                {
                    "type": "text",
                    "text": key_1,
                    "size": "xs",
                    "color": "#aaaaaa",
                    "flex": 0,
                },
                {
                    "type": "text",
                    "text": val_1,
                    "color": "#aaaaaa",
                    "size": "xs",
                    "align": "end",
                },
            ],
        }
    ]
    return bubble


def insert_body_contents_SEP(bubble):
    bubble["body"]["contents"].append({"type": "separator", "margin": "xxl"})
    return bubble


def insert_parcel_search_result(search_result, carousel_container):
    for i, result in enumerate(search_result):
        _id  = result['_id']
        dist = result["districtName"]
        sect = result["sectionName"]
        prcl = result["prcl"]
        luz  = result['landUseZoning']
        lut  = result['landUseType']
        applicants = result["applicants"]
        
        bubble = create_bubble()
        bubble = insert_body_contents_TITLE(bubble, 
                                            f'RESULT {i+1}',
                                            f"{dist}{sect}{prcl}地號",
                                            f"{luz} - {lut}")
        bubble = insert_body_contents_SEP(bubble)

        for a in applicants:
            name = a["name"]
            cap = float(a["capacity"].replace(',', ''))
            area = float(a["caseArea"].replace(',', ''))
            stat = a["status"]

            bubble = insert_body_contents_ITEM(bubble, 
                                               name, 
                                               "設置容量", f"{cap:,.2f}  kW",
                                               "土地面積", f"{area:,.2f}  m2",
                                               "案件狀態", stat)
            bubble = insert_body_contents_SEP(bubble)

        bubble = insert_body_contents_FOOTER(bubble, 
                                             "PARCEL ID", f"#{_id}")
        carousel_container["contents"].append(bubble)


def insert_applicant_search_result(search_result, carousel_container):
    for i, result in enumerate(search_result):
        if i >= 11: break

        _id  = str(result['_id'])
        sess = result['session']
        name = result['name']
        cap  = float(result['capacity'].replace(',', ''))
        area = float(result['caseArea'].replace(',', ''))
        stat = result['status']
        top_color = "#46844f" if stat == '已核准' else "#C28285"
        
        bubble = create_bubble()
        bubble = insert_body_contents_TITLE(bubble, 
                                            stat,
                                            name,
                                            f"第 {sess} 次聯審會議",
                                            top_color=top_color)
        
            
        
        bubble = insert_body_contents_SEP(bubble)
        bubble = insert_body_contents_ITEM(bubble,
                                           "案件資訊概覽",
                                           "設置容量", f"{cap:,.2f}  kW",
                                           "土地面積", f"{area:,.2f}  m2",
                                           "---", "---")
        bubble = insert_body_contents_SEP(bubble)
        bubble = insert_body_contents_FOOTER(bubble, 
                                             "ID", f"#{_id}")
        
        carousel_container["contents"].append(bubble)
