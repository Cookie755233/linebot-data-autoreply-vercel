
from msg.carousel import Carousel, Bubble


def reply_applicant_search_results(results):
    carousel = Carousel()

    for i, result in enumerate(results):
        print(i, result["applicantName"])
        if i >= 11 : break
        
        prsn   = result['PRSN']
        ersn   = result['ERSN'] if isinstance(result['ERSN'], str) else '-'
        appl   = result["applicantName"]
        addr   = result['address'] if isinstance(result['address'], str) else '-'
        pos    = result['position']
        type_  = result['type']
        tc     = result['totalCapacity']
        la     = result['landArea']
        res    = result['result']
        stat   = result['status']
        tc_E   = result['totalCapacity_ER']
        la_E   = result['landArea_ER']
        
        lng, lat   = result['center']['coordinates']
        stat_color = "#46844f" if res == '核准' else "#C28285"
        
        bubble = Bubble()
        bubble.insert_body_contents_TITLE(f'{res} - {stat}', 
                                          appl,
                                          f'地址: {addr}',
                                          top_color=stat_color)
        
        bubble.insert_body_contents_ITEM('申請人詳細資訊',
                                         '設置類型', f'{pos}-{type_}',
                                         '設置容量', f'{tc_E:,.2f} / {tc:,.2f} kW',
                                         '土地面積', f'{la_E:,.2f} / {la:,.2f} M2',
                                         )
        bubble.insert_body_contents_SEP()
        bubble.insert_body_contents_FOOTER('ID', f'{ersn} / {prsn}')
        bubble.insert_footer_contents_BOTTON(lng, lat)

        carousel.insert_bubble(bubble.bubble)

    return carousel.container