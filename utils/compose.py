
from flex.carousel import Carousel, Bubble


def compose_applicant_results(results):
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
        carousel.insert_bubble(bubble.bubble)

    return carousel.container


def compose_applicant_nearby_results(results):
    #! [ ({applicants}, {geo_results}), ... ]
    carousel = Carousel()
    for i, (applicant, geo_results) in enumerate(results):
        if i >= 11: break
        prsn   = applicant['PRSN']
        appl   = applicant["applicantName"]
        res    = applicant['result']
        stat   = applicant['status']
        stat_color = "#46844f" if res == '核准' else "#C28285"
        geo_result_cnt = len(geo_results)
        
        bubble = Bubble()
        bubble.insert_body_contents_TITLE(f'{res} - {stat}', 
                                          appl,
                                          f'共找到 {geo_result_cnt} 筆鄰近案場',
                                          top_color=stat_color,
                                          top_right_text=prsn)
        
        for j, geo_result in enumerate(geo_results):
            n = geo_result['applicantName']
            p = geo_result['position']
            t = geo_result['type']
            r = geo_result['result']
            s = geo_result['status']
            c = geo_result['totalCapacity']
            a = geo_result['landArea']
            d = geo_result['distance']
            
            clr = "#46844f" if r == '核准' else "#C28285"
            bubble.insert_body_contents_ITEM(f'{j+1}. {n}',
                                         '設置類型', f'{p} - {t}',
                                         '案件狀態', f'{r} - {s}',
                                         '面積/容量', f'{a:,.0f} M2 / {c:,.0f} kW',
                                         '距離', f'{d} 公尺',
                                         subtitle_color=clr,
                                         item_size='xxs')
            
            if j+1 != len(geo_results):
                bubble.insert_body_contents_SEP()
        
        carousel.insert_bubble(bubble.bubble)
        
    return carousel.container



def compose_parcel_results(results):
    carousel = Carousel()
    
    for i, result in enumerate(results):
        if i >= 11: break
        
        luz  = result['landUseZoning']
        lut  = result['landUseType']
        lng, lat = result['location']['coordinates']

        parcel_string = f"{result['districtName']}{result['sectionName']}{result['prcl']}"

        bubble = Bubble()

        bubble.insert_body_contents_TITLE(
            f'第 {i+1} 筆近似地號',
            f'{parcel_string}號',
            f'{luz} - {lut}'
            )

        related_applicants = result['relatedApplicants']
        for j, applicant in enumerate(related_applicants):
            appl   = applicant["applicantName"]
            pos    = applicant['position']
            type_  = applicant['type']
            tc     = applicant['totalCapacity']
            la     = applicant['landArea']
            res    = applicant['result']
            # stat   = applicant['status']
            tc_E   = applicant['totalCapacity_ER']
            la_E   = applicant['landArea_ER']

            stat_color = "#46844f" if res == '核准' else "#C28285"
            
            bubble.insert_body_contents_ITEM(
                f'{j+1}. {appl}',
                '設置類型', f'{pos}-{type_}',
                '設置容量', f'{tc_E:,.2f} / {tc:,.2f} kW',
                '土地面積', f'{la_E:,.2f} / {la:,.2f} M2',
                subtitle_color=stat_color
                )

            if j+1 != len(related_applicants):
                bubble.insert_body_contents_SEP()

        bubble.insert_footer_contents_BOTTON(lng, lat)
        carousel.insert_bubble(bubble.bubble)
        
    return carousel.container


def compose_parcel_nearby_results(results):
    carousel = Carousel()

    for i, (parcel, geo_results) in enumerate(results):
        if i >= 11: break
        
        luz  = parcel['landUseZoning']
        lut  = parcel['landUseType']
        lng, lat = parcel['location']['coordinates']

        parcel_string = f"{parcel['districtName']}{parcel['sectionName']}{parcel['prcl']}"

        bubble = Bubble()

        bubble.insert_body_contents_TITLE(
            f'第 {i+1} 筆近似地號', 
            f'{parcel_string}號',
            f'{luz} - {lut}' #TODO maybe add "within how many distance"-> how to pass param into func??
            )
        
        if not geo_results:
            bubble.insert_body_contents_ITEM('無鄰近案場', subtitle_color='#C28285')


        for j, geo_result in enumerate(geo_results):
            if j >= 5: 
                bubble.insert_body_contents_FOOTER(f'共計{len(geo_results)}件鄰近案場，顯示{j+1}件', '-')
                break
            
            n = geo_result['applicantName']
            p = geo_result['position']
            t = geo_result['type']
            r = geo_result['result']
            # s = geo_result['status']
            c = geo_result['totalCapacity']
            a = geo_result['landArea']
            d = geo_result['distance']

            clr = "#46844f" if r == '核准' else "#C28285"
            
            bubble.insert_body_contents_ITEM(f'{j+1}. {n} ({p}-{t})',
                                         '面積/容量', f'{a:,.0f} M2 / {c:,.0f} kW',
                                         '距離', f'{d} 公尺',
                                         subtitle_color=clr,
                                         item_size='xxs')
            
            if j+1 != len(geo_results):
                bubble.insert_body_contents_SEP()

        bubble.insert_footer_contents_BOTTON(lng, lat)

        carousel.insert_bubble(bubble.bubble)

    return carousel.container