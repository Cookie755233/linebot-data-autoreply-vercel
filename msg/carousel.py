
def create_bubble():
    return {
        "type": "bubble",
        "body": {"type": "box", 
                 "layout": "vertical",
                 "contents": []},
        "styles": {"footer": {"separator": True}}
    }


def insert_body_contents_TITLE(bubble, dist, sect, prcl, i, cnt):
    bubble['body']['contents'] += [
        {
            "type": "text",
            "text": f"RESULT {i+1}",
            "weight": "bold",
            "color": "#46844f",
            "size": "xs",
        },
        {
            "type": "text",
            "text": f"{dist}{sect}{prcl}地號",
            "weight": "bold",
            "size": "lg",
            "margin": "md",
        },
        {
            "type": "text",
            "text": f"共計 {cnt} 個申請案件",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
        },
    ]
    return bubble


def insert_body_contents_SEP(bubble):
    bubble['body']['contents'].append(
        {"type": "separator", "margin": "xxl"}
    )
    return bubble


def insert_body_contents_ITEM(bubble, name, cap, area, stat):
    bubble['body']['contents'] += [
        {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": f"{name}",
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
                            "text": "設置容量",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": f"{cap:,.2f}  kW",
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
                            "text": "土地面積",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": f"{area:,.2f}  m2",
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
                            "text": "案件狀態",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0,
                        },
                        {
                            "type": "text",
                            "text": f"{stat}",
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


def insert_search_result(search_result, carousel_container):
    for i, result in enumerate(search_result):
        dist = result["districtName"]
        sect = result["sectionName"]
        prcl = result["prcl"]
        cnt = int(result["applicantCount"])
        applicants = result["applicants"]
        
        bubble = create_bubble()
        bubble = insert_body_contents_TITLE(bubble, dist, sect, prcl, i, cnt)
        bubble = insert_body_contents_SEP(bubble)
        
        for j, a in enumerate(applicants):
            name = a["name"]
            cap = float(a["capacity"])
            area = float(a["caseArea"])
            stat = a['status']
            bubble = insert_body_contents_ITEM(bubble, name, cap, area, stat)
            
            if j < cnt - 1:
                bubble = insert_body_contents_SEP(bubble)
        carousel_container["contents"].append(bubble)
