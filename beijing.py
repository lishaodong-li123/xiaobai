"""
 -*- coding: utf-8 -*-
 @Author     :            xiaobai
 @Time       :            2025/1/17 1:53 下午
 @File       :            xiaobai
"""

import requests
import random
import time
import re
from bs4 import BeautifulSoup
import pymysql
import mysql_info

print('开始链接数据库')
connect = pymysql.connect(
    host=mysql_info.mysql_info_test['host'],
    user=mysql_info.mysql_info_test['user'],
    password=mysql_info.mysql_info_test['password'],
    port=mysql_info.mysql_info_test['port'],
    db=mysql_info.mysql_info_test['db'],
    charset=mysql_info.mysql_info_test['charset']
)
cursor = connect.cursor()
print('链接成功。。。。')


if __name__ == '__main__':

    for i in range(0,25):
        print(f'当前正在执行第{i}页')
        USER_AGENTS = [

                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",

                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",

                "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",

                "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",

                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",

                "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",

                "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",

                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",

                "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",

                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",

                "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",

                "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",

                "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",

                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",

                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",

                "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",

            ]
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }
        time.sleep(2)
        # 规范性文件
        # 'https://czj.beijing.gov.cn/zwxx/2024zcwj/2024gfxwj/index.html'
        # 其他文件
        ''
        if i == 0:
            url = 'https://czj.beijing.gov.cn/zwxx/2024zcwj/2024qtwj/index.html'
        else:
            url = f'https://czj.beijing.gov.cn/zwxx/2024zcwj/2024qtwj/index_{i}.html'
        response_source = requests.get(url, headers=headers)
        res_json2 = response_source.content.decode('utf-8')
        bss = BeautifulSoup(res_json2, 'html5lib')
        li_list = bss.select('div.ul-back > ul > li')
        for li in li_list:
            # 详情链接
            # href = str(li.select('a')[0].get('href')).strip().replace('./','https://czj.beijing.gov.cn/zwxx/2024zcwj/2024gfxwj/')
            href = str(li.select('a')[0].get('href')).strip().replace('./','https://czj.beijing.gov.cn/zwxx/2024zcwj/2024qtwj/')
            # 标题名称
            title = str(li.select('a')[0].text).strip()
            publishDate = li.select('span')[0].text.strip()
            # print(href,title,publishDate)
            sqlcmd = "select id from sasac_policy where href = %s"
            # 执行SQL语句
            cursor.execute(sqlcmd, href)
            # 获取所有记录列表
            results = cursor.fetchall()
            if len(results) > 0:
                continue
            else:
                headerss = {
                    'User-Agent': random.choice(USER_AGENTS)
                }
                response = requests.get(f'{href}',headers=headers)
                source = response.content.decode('utf-8')
                bss2 = BeautifulSoup(source, 'html5lib')
                li = bss2.select('ul.doc-info.clearfix')
                if len(li) > 0:
                    xiangqing = str(li[0].text).replace('\n', '').strip()
                    # print(xiangqing)
                    laiyuan = ''
                    # 索引号
                    indexNum = ''
                    # 主题分类
                    themeType = str(re.findall('\[主题分类](.*?)\[发文机构]', xiangqing)[0]).strip()
                    # 发文机关
                    IssuingAgency = str(re.findall('\[发文机构](.*?)\[联合发文单位]', xiangqing)[0]).strip()
                    # 成文日期
                    writtenDate = str(re.findall('\[成文日期](.*?)\[发文字号]', xiangqing)[0]).split('.noN2{')[0].strip()
                    # 发文字号
                    lssuingNum = str(re.findall('\[发文字号](.*?)\[废止日期]', xiangqing)[0]).strip()
                    # 实施日期
                    carryDate = str(re.findall('\[实施日期](.*?)\[成文日期]', xiangqing)[0]).split('.noN1{')[0].strip()
                    # 废止日期
                    annulDate = str(re.findall('\[废止日期](.*?)\[发布日期]', xiangqing)[0]).strip()
                    # 时效
                    if '[有效性]' in xiangqing:
                        policyPec = str(xiangqing).split('[有效性]')[1].split('.doc-info {')[0].strip()
                    else:
                        policyPec = ''
                    # 来源网站
                    webSource = 'https://czj.beijing.gov.cn/'
                    # 政策分类
                    policyType = '本局其他文件'
                    section = '财政局'
                    # 省份
                    province = '北京市'
                    str_tt = []
                    div_list1 = bss2.select('div.view.TRS_UEDITOR.trs_paper_default.trs_web.trs_key4format')
                    div_list2 = bss2.select('div.view.TRS_UEDITOR.trs_paper_default.trs_web')
                    if len(div_list1) > 0:
                        div_list = div_list1
                    elif len(div_list2) > 0:
                        div_list = div_list1
                    else:
                        continue
                    if len(div_list) > 0:
                        if 'img' in str(div_list) or 'png' in str(div_list) or 'table' in str(div_list):
                            mark = 1
                            str_tt = str_tt
                        else:
                            mark = 0
                            for d in div_list:
                                p_list1 = d.select('p')
                                p_list2 = d.select('div > p')
                                if len(p_list2) > 0:
                                    p_list = p_list2
                                elif len(p_list1) > 0:
                                    p_list = p_list1
                                for p in p_list:
                                    # print(p.text)
                                    bs2_list = str(p.text).strip().split(' ')
                                    # print(bs2_list)
                                    for bs2 in bs2_list:
                                        if bs2 < u'\u4e00' or bs2 > u'\u9fff' or u'\u4e00' <= bs2 <= u'\u9fff':
                                            bs3 = ''.join(bs2.split())
                                            str_tt.append({"text": bs3})
                    jsj = '{"title":"' + title + '","shijian":"' + str(publishDate) + '","texts":' + str(str_tt) + '}'
                    bsss = jsj.replace("'", '"')
                    if writtenDate == '':
                        try:
                            sql = (
                                'insert into sasac_policy(lssuingNum,mark,province,carryDate,annulDate,section,href,indexNum,themeType,IssuingAgency,title,publishDate,mainSource,laiyuan,webSource,policyType,policyPec)' 'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
                            canshu = (
                                lssuingNum, mark, province, carryDate, annulDate, section, href, indexNum, themeType,
                                IssuingAgency,
                                title, publishDate, bsss, laiyuan,
                                webSource, policyType,
                                policyPec)
                            cursor.execute(sql, canshu)
                            connect.commit()
                            print('保存成功！！！！')
                        except Exception as e:
                            print(e)
                    else:
                        try:
                            sql = (
                                'insert into sasac_policy(lssuingNum,mark,province,carryDate,annulDate,section,href,writtenDate,indexNum,themeType,IssuingAgency,title,publishDate,mainSource,laiyuan,webSource,policyType,policyPec)' 'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
                            canshu = (
                                lssuingNum, mark, province, carryDate, annulDate, section, href, writtenDate, indexNum,
                                themeType,
                                IssuingAgency, title, publishDate,
                                bsss, laiyuan, webSource,
                                policyType, policyPec)
                            cursor.execute(sql, canshu)
                            connect.commit()
                            print('保存成功！！！！')
                        except Exception as e:
                            print(e)
