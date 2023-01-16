import argparse
import os

from linebot import LineBotApi
from linebot.models.actions import MessageAction, PostbackAction, URIAction, DatetimePickerAction, RichMenuSwitchAction, CameraAction
from linebot.models.rich_menu import RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize


# rich_menu_alias = "my-richmenu"
rich_menu = RichMenu(
    size=RichMenuSize(width=2500, height=1686),  # 大小
    selected=True,  # 預設開啟或關閉
    name="my-richmenu",  # 名稱
    chat_bar_text="選單",  # 下方選單名稱
    areas=[
        # 左上
        RichMenuArea(
            RichMenuBounds(x=0, y=0, width=1250, height=843),
            MessageAction(label="左上按鈕", text="按下左上")
        ),
        # 右上
        RichMenuArea(
            RichMenuBounds(x=1251, y=0, width=1250, height=843),
            MessageAction(label="右上按鈕", text="按下右上")
        ),
        # 左下
        RichMenuArea(
            RichMenuBounds(x=0, y=844, width=1250, height=843),
            MessageAction(label="左下按鈕", text="按下左下")
        ),
        # 右下
        RichMenuArea(
            RichMenuBounds(x=1251, y=844, width=1250, height=843), 
            action=DatetimePickerAction(label="右下按鈕", data="按下右下", mode='date')
            # MessageAction(label="右下按鈕", text="右下按鈕")
        )
    ]
)


if __name__ == "__main__":
    line_bot_api = LineBotApi("rfuE7VDpCL5uW04CQyQe3gcPdOnthMltWaPpE51agJxL4+d1GqhXF76cin4xITYwuG8N6kecl23tvjkeN7DzgLpUxQ/hvu3LveTNuZiVkmj+gKS0ItL3q4ZMTgNrCJz0kKnpqLIk/jCSzIxJUxsoMgdB04t89/1O/w1cDnyilFU=")

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true", help="Create a new RichMenu")
    parser.add_argument("-g", "--get", action="store_true", help="Get default RichMenu")
    parser.add_argument("-l", "--list", action="store_true", help="Get all RichMenu")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete default RichMenu")
    args = parser.parse_args()
    
    if args.create:
        richmenu_id = line_bot_api.create_rich_menu(rich_menu)
        with open("CMYK.jpg", "rb") as fp:
            line_bot_api.set_rich_menu_image(
                richmenu_id, content_type="image/jpeg", content=fp)
        line_bot_api.set_default_rich_menu(richmenu_id)
    elif args.get:
        print(line_bot_api.get_rich_menu(line_bot_api.get_default_rich_menu()))
    elif args.list:
        for r in line_bot_api.get_rich_menu_list():
            print(r)
    elif args.delete:
        line_bot_api.delete_rich_menu(line_bot_api.get_default_rich_menu())