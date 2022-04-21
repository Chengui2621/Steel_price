import requests
from lxml import etree
import re
import pandas as pd


# 硅钢
def get_data_guigang():
    url = 'https://list1.mysteel.com/market/p-437-----010106-0-01010401-------1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Cookie': '_last_loginuname=goodbaby123; _login_psd=3ba7e75e56a34c01b56c65f10e8901b16; _rememberStatus=true; Hm_lvt_1c4432afacfa2301369a5625795031b8=1649222144; allHistory=%5B%22%E7%94%B5%E9%95%80%E4%B8%9D%22%5D; href=http%3A%2F%2Fguigang.mysteel.com%2F; accessId=5d36a9e0-919c-11e9-903c-ab24dbab411b; pageViewNum=3; _last_ch_r_t=1649397611208; fingerprint=a64ff2e9c89fde087b97042290980c0c; _login_token=3b4df51e8f109f30b5166808f3ce710b; _login_uid=2243467; _login_mid=3057897; _login_ip=183.129.214.218; 3b4df51e8f109f30b5166808f3ce710b=1%3D10%262%3D10%26catalog%3D010102%2C010103; Hm_lpvt_1c4432afacfa2301369a5625795031b8=1649398288'}
    response = requests.get(url)
    url_tree = etree.HTML(response.text)
    next_url = url_tree.xpath('//*[@id="articleList"]/ul/li[1]/a/@href')[0]
    detail_response = requests.get(next_url, headers=headers)
    detail_url_tree = etree.HTML(detail_response.text)
    # 获取数据标题和日期
    detail_title = detail_url_tree.xpath('//*[@id="articleContent"]/h1/text()')[0]
    detail_data_date = re.search('([0-9]+?月[0-9]+?日)', detail_title).group()
    detail_tr_list = detail_url_tree.xpath('//*[@id="marketTable"]/tr')
    detail_tr_list = [detail_tr_list[15], detail_tr_list[5], detail_tr_list[17], detail_tr_list[6], detail_tr_list[14]]

    data_list = []
    for tr in detail_tr_list:
        td_list = tr.xpath('./td[@align]')
        td_list = [td_list[0], td_list[1], td_list[2], td_list[3], td_list[4]]
        single_data_list = []
        for td in td_list:
            data = td.xpath('./text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
            single_data_list.append(data)
        data_list.append(single_data_list)
    df = pd.DataFrame(data_list)
    table_title = ['武钢50WW800', '武钢50WW470', '首钢50SW800', '宝钢B50470-A', '宝钢B50A800']
    df.columns = ['品名', '规格', '材质', '钢厂', '价格']
    df['表格表头'] = table_title
    # print(df)
    return df


# 冷板
def get_data_lengban():
    url = 'https://list1.mysteel.com/market/p-221-----010104-0-010101-------1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Cookie': '_last_loginuname=goodbaby123; _login_psd=3ba7e75e56a34c01b56c65f10e8901b16; _rememberStatus=true; Hm_lvt_1c4432afacfa2301369a5625795031b8=1649222144; allHistory=%5B%22%E7%94%B5%E9%95%80%E4%B8%9D%22%5D; href=http%3A%2F%2Fguigang.mysteel.com%2F; accessId=5d36a9e0-919c-11e9-903c-ab24dbab411b; pageViewNum=3; _last_ch_r_t=1649397611208; fingerprint=a64ff2e9c89fde087b97042290980c0c; _login_token=3b4df51e8f109f30b5166808f3ce710b; _login_uid=2243467; _login_mid=3057897; _login_ip=183.129.214.218; 3b4df51e8f109f30b5166808f3ce710b=1%3D10%262%3D10%26catalog%3D010102%2C010103; Hm_lpvt_1c4432afacfa2301369a5625795031b8=1649398288'}
    response = requests.get(url)
    url_tree = etree.HTML(response.text)
    check_title = url_tree.xpath('//*[@id="articleList"]/ul/li[1]/a/text()')[0]
    if '板卷' in check_title:
        next_url = url_tree.xpath('//*[@id="articleList"]/ul/li[1]/a/@href')[0]
    else:
        next_url = url_tree.xpath('//*[@id="articleList"]/ul/li[2]/a/@href')[0]
    detail_response = requests.get(next_url, headers=headers)
    detail_url_tree = etree.HTML(detail_response.text)
    # 获取数据标题和日期
    detail_title = detail_url_tree.xpath('//*[@id="articleContent"]/h1/text()')[0]
    detail_data_date = re.search('([0-9]+?月[0-9]+?日)', detail_title).group()
    detail_data_month = detail_data_date.split('月')[0] + '月份（吨）'
    detail_data_day = re.search('月(.*?)日', detail_data_date).group(1) + '号'
    detail_tr_list = detail_url_tree.xpath('//*[@id="marketTable"]/tr')
    detail_tr_list = [detail_tr_list[2], detail_tr_list[3], detail_tr_list[4], detail_tr_list[5],
                      detail_tr_list[6], detail_tr_list[7], detail_tr_list[8], detail_tr_list[9]]

    data_list = []
    for tr in detail_tr_list:
        td_list = tr.xpath('./td[@align]')
        td_list = [td_list[0], td_list[1], td_list[2], td_list[3], td_list[4]]
        single_data_list = []
        for td in td_list:
            data = td.xpath('./text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
            single_data_list.append(data)
        data_list.append(single_data_list)
    df = pd.DataFrame(data_list)
    table_title = ['0.6 冷板', '0.8 冷板', '1.0 冷板', '鞍钢冷板1.2', '1.5 冷板', '2.0冷板/DC01', '2.5冷板/DC01', '3.0冷板/DC01']
    df.columns = ['品名', '规格', '材质', '产地', '价格']
    df['表格表头'] = table_title
    # print(df)
    return df


# 热板
def get_data_reban():
    url = 'https://list1.mysteel.com/market/p-231-----010103-0-010101-------1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Cookie': '_last_loginuname=goodbaby123; _login_psd=3ba7e75e56a34c01b56c65f10e8901b16; _rememberStatus=true; Hm_lvt_1c4432afacfa2301369a5625795031b8=1649222144; allHistory=%5B%22%E7%94%B5%E9%95%80%E4%B8%9D%22%5D; href=http%3A%2F%2Fguigang.mysteel.com%2F; accessId=5d36a9e0-919c-11e9-903c-ab24dbab411b; pageViewNum=3; _last_ch_r_t=1649397611208; fingerprint=a64ff2e9c89fde087b97042290980c0c; _login_token=3b4df51e8f109f30b5166808f3ce710b; _login_uid=2243467; _login_mid=3057897; _login_ip=183.129.214.218; 3b4df51e8f109f30b5166808f3ce710b=1%3D10%262%3D10%26catalog%3D010102%2C010103; Hm_lpvt_1c4432afacfa2301369a5625795031b8=1649398288'}
    response = requests.get(url)
    url_tree = etree.HTML(response.text)
    url_list = url_tree.xpath('//*[@id="articleList"]/ul/li')
    first_title = url_list[0].xpath('./a/text()')[0]
    title_check = re.search('([0-9]+?月[0-9]+?日)', first_title).group()
    for li in url_list:
        next_title = li.xpath('./a/text()')
        if next_title:
            if '热轧板卷' in next_title[0] and '（' not in next_title[0] and '(' not in next_title[0] and title_check in \
                    next_title[0]:
                # print(next_title[0])
                next_url = li.xpath('./a/@href')[0]

    detail_response = requests.get(next_url, headers=headers)
    detail_url_tree = etree.HTML(detail_response.text)
    # 获取数据标题和日期
    detail_title = detail_url_tree.xpath('//*[@id="articleContent"]/h1/text()')[0]
    detail_data_date = re.search('([0-9]+?月[0-9]+?日)', detail_title).group()
    detail_data_month = detail_data_date.split('月')[0] + '月份（吨）'
    detail_data_day = detail_data_date.split('月')[1][0] + '号'
    detail_tr_list = detail_url_tree.xpath('//*[@id="marketTable"]/tr')
    detail_tr_list = [detail_tr_list[38], detail_tr_list[44], detail_tr_list[50], detail_tr_list[68]]

    data_list = []
    for tr in detail_tr_list:
        td_list = tr.xpath('./td[@align]')
        td_list = [td_list[0], td_list[1], td_list[2], td_list[3], td_list[4]]
        single_data_list = []
        for td in td_list:
            data = td.xpath('./text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
            single_data_list.append(data)
        data_list.append(single_data_list)
    df = pd.DataFrame(data_list)
    table_title = ['4.0 Q235热板', '5.0 Q235热板', '6.0 Q235热板', '10.0 Q235热板']
    df.columns = ['品名', '规格', '材质', '钢厂', '价格']
    df['表格表头'] = table_title
    # print(df)
    return df


# 酸洗板
def get_data_suanxiban():
    url = 'https://list1.mysteel.com/market/p-231-----010103-0-010101-------1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Cookie': '_last_loginuname=goodbaby123; _login_psd=3ba7e75e56a34c01b56c65f10e8901b16; _rememberStatus=true; Hm_lvt_1c4432afacfa2301369a5625795031b8=1649222144; allHistory=%5B%22%E7%94%B5%E9%95%80%E4%B8%9D%22%5D; href=http%3A%2F%2Fguigang.mysteel.com%2F; accessId=5d36a9e0-919c-11e9-903c-ab24dbab411b; pageViewNum=3; _last_ch_r_t=1649397611208; fingerprint=a64ff2e9c89fde087b97042290980c0c; _login_token=3b4df51e8f109f30b5166808f3ce710b; _login_uid=2243467; _login_mid=3057897; _login_ip=183.129.214.218; 3b4df51e8f109f30b5166808f3ce710b=1%3D10%262%3D10%26catalog%3D010102%2C010103; Hm_lpvt_1c4432afacfa2301369a5625795031b8=1649398288'}

    response = requests.get(url)
    url_tree = etree.HTML(response.text)
    url_list = url_tree.xpath('//*[@id="articleList"]/ul/li')
    first_title = url_list[0].xpath('./a/text()')[0]
    title_check = re.search('([0-9]+?月[0-9]+?日)', first_title).group()
    for li in url_list:
        next_title = li.xpath('./a/text()')
        if next_title:
            if '热轧酸洗卷' in next_title[0] and '（' not in next_title[0] and '(' not in next_title[0] and title_check in \
                    next_title[0]:
                # print(next_title[0])
                next_url = li.xpath('./a/@href')[0]

    detail_response = requests.get(next_url, headers=headers)
    detail_url_tree = etree.HTML(detail_response.text)
    # 获取数据标题和日期
    detail_title = detail_url_tree.xpath('//*[@id="articleContent"]/h1/text()')[0]
    detail_data_date = re.search('([0-9]+?月[0-9]+?日)', detail_title).group()
    detail_data_month = detail_data_date.split('月')[0] + '月份（吨）'
    detail_data_day = detail_data_date.split('月')[1][0] + '号'
    detail_tr_list = detail_url_tree.xpath('//*[@id="marketTable"]/tr')
    detail_tr_list = [detail_tr_list[21], detail_tr_list[4]]

    data_list = []
    for tr in detail_tr_list:
        td_list = tr.xpath('./td[@align]')
        td_list = [td_list[0], td_list[1], td_list[2], td_list[3], td_list[4]]
        single_data_list = []
        for td in td_list:
            data = td.xpath('./text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
            single_data_list.append(data)
        data_list.append(single_data_list)
    df = pd.DataFrame(data_list)
    table_title = ['4.0酸洗板', '2.0酸洗板']
    df.columns = ['品名', '规格', '材质', '钢厂', '价格']
    df['表格表头'] = table_title
    # print(df)
    return df


# 镀锌板
def get_data_duxinban():
    url = 'https://list1.mysteel.com/market/p-221-----01010501-0-010101-------1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Cookie': '_last_loginuname=goodbaby123; _login_psd=3ba7e75e56a34c01b56c65f10e8901b16; _rememberStatus=true; Hm_lvt_1c4432afacfa2301369a5625795031b8=1649222144; allHistory=%5B%22%E7%94%B5%E9%95%80%E4%B8%9D%22%5D; href=http%3A%2F%2Fguigang.mysteel.com%2F; accessId=5d36a9e0-919c-11e9-903c-ab24dbab411b; pageViewNum=3; _last_ch_r_t=1649397611208; fingerprint=a64ff2e9c89fde087b97042290980c0c; _login_token=3b4df51e8f109f30b5166808f3ce710b; _login_uid=2243467; _login_mid=3057897; _login_ip=183.129.214.218; 3b4df51e8f109f30b5166808f3ce710b=1%3D10%262%3D10%26catalog%3D010102%2C010103; Hm_lpvt_1c4432afacfa2301369a5625795031b8=1649398288'}

    response = requests.get(url)
    url_tree = etree.HTML(response.text)
    url_check_title = url_tree.xpath('//*[@id="articleList"]/ul/li[1]/a/text()')[0]
    # 判断是否为更新的数据
    if url_check_title.find("（") == -1:
        next_url = url_tree.xpath('//*[@id="articleList"]/ul/li[1]/a/@href')[0]
    else:
        next_url = url_tree.xpath('//*[@id="articleList"]/ul/li[2]/a/@href')[0]
    detail_response = requests.get(next_url, headers=headers)
    detail_url_tree = etree.HTML(detail_response.text)
    # 获取数据标题和日期
    detail_title = detail_url_tree.xpath('//*[@id="articleContent"]/h1/text()')[0]
    detail_data_date = re.search('([0-9]+?月[0-9]+?日)', detail_title).group()
    detail_data_month = detail_data_date.split('月')[0] + '月份（吨）'
    detail_data_day = detail_data_date.split('月')[1][0] + '号'
    detail_tr_list = detail_url_tree.xpath('//*[@id="marketTable"]/tr')
    detail_tr_list = [detail_tr_list[24], detail_tr_list[25], detail_tr_list[26], detail_tr_list[36]]

    data_list = []
    for tr in detail_tr_list:
        td_list = tr.xpath('./td[@align]')
        td_list = [td_list[0], td_list[1], td_list[2], td_list[3], td_list[4]]
        single_data_list = []
        for td in td_list:
            data = td.xpath('./text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
            single_data_list.append(data)
        data_list.append(single_data_list)
    df = pd.DataFrame(data_list)
    table_title = ['1.0 SGCC普通无花镀锌板/鞍钢', '1.2 SGCC普通无花镀锌板/鞍钢',
                   '1.5 SGCC普通无花镀锌板/鞍钢', '2.0 SGCC普通无花镀锌板/鞍钢']
    df.columns = ['品名', '规格', '材质', '钢厂', '价格']
    df['表格表头'] = table_title
    # print(df)
    return df


# 电镀丝
def get_data_diandusi():
    url = 'https://list1.mysteel.com/market/p-405-----010211-0-0101040401-------1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Cookie': '_last_loginuname=goodbaby123; _login_psd=3ba7e75e56a34c01b56c65f10e8901b16; _rememberStatus=true; Hm_lvt_1c4432afacfa2301369a5625795031b8=1649222144; allHistory=%5B%22%E7%94%B5%E9%95%80%E4%B8%9D%22%5D; href=http%3A%2F%2Fguigang.mysteel.com%2F; accessId=5d36a9e0-919c-11e9-903c-ab24dbab411b; pageViewNum=3; _last_ch_r_t=1649397611208; fingerprint=a64ff2e9c89fde087b97042290980c0c; _login_token=3b4df51e8f109f30b5166808f3ce710b; _login_uid=2243467; _login_mid=3057897; _login_ip=183.129.214.218; 3b4df51e8f109f30b5166808f3ce710b=1%3D10%262%3D10%26catalog%3D010102%2C010103; Hm_lpvt_1c4432afacfa2301369a5625795031b8=1649398288'}

    response = requests.get(url)
    url_tree = etree.HTML(response.text)
    url_check_title = url_tree.xpath('//*[@id="articleList"]/ul/li[1]/a/text()')[0]
    # 判断是否为更新的数据
    if url_check_title.find("（") == -1:
        next_url = url_tree.xpath('//*[@id="articleList"]/ul/li[1]/a/@href')[0]
    else:
        next_url = url_tree.xpath('//*[@id="articleList"]/ul/li[2]/a/@href')[0]
    detail_response = requests.get(next_url, headers=headers)
    detail_url_tree = etree.HTML(detail_response.text)
    # 获取数据标题和日期
    detail_title = detail_url_tree.xpath('//*[@id="articleContent"]/h1/text()')[0]
    detail_data_date = re.search('([0-9]+?月[0-9]+?日)', detail_title).group()
    detail_data_month = detail_data_date.split('月')[0] + '月份（吨）'
    detail_data_day = detail_data_date.split('月')[1][0] + '号'
    detail_tr_list = detail_url_tree.xpath('//*[@id="marketTable"]/tr')
    detail_tr_diandusi = detail_tr_list[3]

    data_list_diandusi = []
    td_list_diandusi = detail_tr_diandusi.xpath('./td[@align]')
    td_list_diandusi = [td_list_diandusi[0], td_list_diandusi[1], td_list_diandusi[3], td_list_diandusi[4],
                        td_list_diandusi[5]]
    single_data_list_diandusi = []
    for td in td_list_diandusi:
        data = td.xpath('./text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        single_data_list_diandusi.append(data)
    data_list_diandusi.append(single_data_list_diandusi)
    df_diandusi = pd.DataFrame(data_list_diandusi)
    df_diandusi.columns = ['钢种', '牌号', '规格', '钢厂', '价格']
    # print(df_diandusi)
    return df_diandusi


# 喷塑丝
def get_data_pensusi():
    url = 'https://list1.mysteel.com/market/p-405-----010211-0-0101040401-------1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Cookie': '_last_loginuname=goodbaby123; _login_psd=3ba7e75e56a34c01b56c65f10e8901b16; _rememberStatus=true; Hm_lvt_1c4432afacfa2301369a5625795031b8=1649222144; allHistory=%5B%22%E7%94%B5%E9%95%80%E4%B8%9D%22%5D; href=http%3A%2F%2Fguigang.mysteel.com%2F; accessId=5d36a9e0-919c-11e9-903c-ab24dbab411b; pageViewNum=3; _last_ch_r_t=1649397611208; fingerprint=a64ff2e9c89fde087b97042290980c0c; _login_token=3b4df51e8f109f30b5166808f3ce710b; _login_uid=2243467; _login_mid=3057897; _login_ip=183.129.214.218; 3b4df51e8f109f30b5166808f3ce710b=1%3D10%262%3D10%26catalog%3D010102%2C010103; Hm_lpvt_1c4432afacfa2301369a5625795031b8=1649398288'}

    response = requests.get(url)
    url_tree = etree.HTML(response.text)
    url_check_title = url_tree.xpath('//*[@id="articleList"]/ul/li[1]/a/text()')[0]
    # 判断是否为更新的数据
    if url_check_title.find("（") == -1:
        next_url = url_tree.xpath('//*[@id="articleList"]/ul/li[1]/a/@href')[0]
    else:
        next_url = url_tree.xpath('//*[@id="articleList"]/ul/li[2]/a/@href')[0]
    detail_response = requests.get(next_url, headers=headers)
    detail_url_tree = etree.HTML(detail_response.text)
    # 获取数据标题和日期
    detail_title = detail_url_tree.xpath('//*[@id="articleContent"]/h1/text()')[0]
    detail_data_date = re.search('([0-9]+?月[0-9]+?日)', detail_title).group()
    detail_data_month = detail_data_date.split('月')[0] + '月份（吨）'
    detail_data_day = detail_data_date.split('月')[1][0] + '号'
    detail_tr_list = detail_url_tree.xpath('//*[@id="marketTable"]/tr')
    detail_tr_pensusi = detail_tr_list[5]

    data_list_pensusi = []
    td_list_pensusi = detail_tr_pensusi.xpath('./td[@align]')
    td_list_pensusi = [td_list_pensusi[0], td_list_pensusi[1], td_list_pensusi[3], td_list_pensusi[4], td_list_pensusi[5]]
    single_data_list_pensusi = []
    for td in td_list_pensusi:
        data = td.xpath('./text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        single_data_list_pensusi.append(data)
    data_list_pensusi.append(single_data_list_pensusi)
    df_pensusi = pd.DataFrame(data_list_pensusi)
    df_pensusi.columns = ['钢种', '牌号', '规格', '钢厂', '价格']
    # print(df_pensusi)
    return df_pensusi
