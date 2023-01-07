
from msg.carousel import Carousel, Bubble


def reply_applicant_search_results(results):
    carousel = Carousel()

    for i, result in enumerate(results):
        if i >= 11 : break
        
        prsn   = result['PRSN']
        ersn   = result['ERSN'] if isinstance(result['ERSN'], str) else '-'
        appl   = result["applicantName"]
        addr   = result['address']
        # luz    = result['landUseZoning']
        # lut    = result['landUseType']
        pos    = result['position']
        type_  = result['type']
        tc     = result['totalCapacity']
        la     = result['landArea']
        stat   = result['status']
        res    = result['result']
        tc_E   = result['totalCapacity_ER'] if ersn!='-' else '-'
        la_E   = result['landArea_ER'] if ersn!='-' else '-'
        
        lng, lat   = result['center']['coordinates']
        stat_color = "#46844f" if stat == '已核准' else "#C28285"
        
        bubble = Bubble()
        bubble.insert_body_contents_TITLE(f'{stat} - {res}', 
                                          appl,
                                          addr,
                                          top_color=stat_color)
        
        bubble.insert_body_contents_ITEM('申請人詳細資訊',
                                         '設置類型', pos+type_,
                                         '設置容量', f'{tc_E} / {tc} kW',
                                         '土地面積', f'{la_E} / {la} M2',
                                        #  '土地使用分區', f'{luz} - {lut}'
                                         )
        bubble.insert_body_contents_SEP()
        bubble.insert_body_contents_FOOTER('ID', f'{ersn}/ {prsn}')
        bubble.insert_footer_contents_BOTTON(lng, lat)
        
        carousel.insert_bubble(bubble.bubble)

    return carousel.container
