
import re

from flex.carousel import Carousel, Bubble


def compose_keyword_results(results):
    carousel = Carousel()

    for i, result in enumerate(results):
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
        # print(
        #     list(map(float, re.findall(
        #         r'[0-9]*[.]?[0-9]+', f"location: {lng}, {lat}")))
        # )
        carousel.insert_bubble(bubble.bubble)

    return carousel.container


def compose_keyword_nearby_results(results):
    #! [ ({applicants}, {geo_results}), ... ]
    carousel = Carousel()
    for i, (applicant, geo_results) in enumerate(results):
        if i >= 11: break
        
        appl   = applicant["applicantName"]
        addr   = applicant['address'] if isinstance(applicant['address'], str) else '-'
        res    = applicant['result']
        stat   = applicant['status']
        stat_color = "#46844f" if res == '核准' else "#C28285"
        
        bubble = Bubble()
        bubble.insert_body_contents_TITLE(f'{res} - {stat}', 
                                          appl,
                                          f'地址: {addr}',
                                          top_color=stat_color)
        
        for j, result in enumerate(geo_results):
            n = result['applicantName']
            p = result['position']
            t = result['type']
            r = result['result']
            s = result['status']
            c = result['totalCapacity']
            a = result['landArea']
            bubble.insert_body_contents_ITEM(f'{j}. {n}',
                                         '設置類型', f'{p} - {t}',
                                         '案件狀態', f'{r} - {s}'
                                         '面積/容量', f'{a:,.0f} M2 / {c:,.0f} kW',
                                         size='xxs')
            
            if j+1 != len(geo_results):
                bubble.insert_body_contents_SEP()
        
        carousel.insert_bubble(bubble.bubble)
        
    return carousel.container

