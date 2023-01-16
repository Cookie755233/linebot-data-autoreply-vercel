### Linebot Actions / Events Map
Action =======================> Event
├── Message action ------------ MessageEvent
|                               ├── TextMessage
|                               ├── StickerMessage
|                               ├── ImageMessage
|                               ├── VideoMessage
|                               ├── AudioMessage
|                               ├── LocationMessage
|                               ├── * Imagemap message
|                               ├── * Template message
|                               ├── FlexMessage
|                               └── FileMessage
├── URI action
├── Camera action (Quick reply Only)
├── Camera roll action (Quick reply Only)
├── Location action (Quick reply Only)
├── Datetime picker action ---- PostbackEvent
├── Postback action ----------- PostbackEvent
└── Richmenu Switch Action ---- PostbackEvent
