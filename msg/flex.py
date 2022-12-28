def reply_flex():
    flex = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "weight": "bold",
                "color": "#1DB446",
                "size": "sm",
                "text": "已核准"
            },
            {
                "type": "text",
                "text": "公雞叫股份有限公司",
                "weight": "bold",
                "size": "xxl",
                "margin": "md"
            },
            {
                "type": "text",
                "text": "台南市七股區七股段000號",
                "size": "xs",
                "color": "#999999",
                "wrap": True
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "xxl",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "土地面積",
                        "size": "sm",
                        "color": "#555555",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "999 ㎡ ",
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                    ]
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
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "999 kW",
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xxl",
                    "contents": [
                    {
                        "type": "text",
                        "text": "土地使用分區",
                        "size": "sm",
                        "color": "#555555"
                    },
                    {
                        "type": "text",
                        "text": "3",
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "size": "sm",
                        "color": "#555555",
                        "text": "土地所有權人"
                    },
                    {
                        "type": "text",
                        "text": "$7.31",
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                    ]
                }
                ]
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                {
                    "type": "text",
                    "text": "同意備案編號 ",
                    "size": "xs",
                    "color": "#aaaaaa",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": "TNN-NMSL69420",
                    "color": "#aaaaaa",
                    "size": "xs",
                    "align": "end"
                }
                ]
            }
            ]
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
    }
    return flex