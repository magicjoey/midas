#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: midas
    @description:银行维护通知
    @version: 2016-12-25 11:06,bank_maintain_task V1.0 
"""
import datetime
from django.core.mail import send_mail
from pyquery import PyQuery as pyq


def crawl(from_date=None):
    maintain_list = {}
    maintain_list['ABC'] = crawl_abc(from_date)
    maintain_list['CCB'] = crawl_ccb(from_date)
    maintain_list['ICBC'] = crawl_icbc(from_date)
    maintain_list['BOC'] = crawl_boc(from_date)
    maintain_list['CMB'] = crawl_cmb(from_date)
    maintain_list['PSBC'] = crawl_psbc(from_date)
    maintain_list['CITIC'] = crawl_citic(from_date)
    maintain_list['CMBC'] = crawl_cmbc(from_date)
    maintain_list['CEB'] = crawl_ceb(from_date)
    maintain_list['COMM'] = crawl_comm(from_date)
    maintain_list['CIB'] = crawl_cib(from_date)
    maintain_list['HXB'] = crawl_hxb(from_date)
    maintain_list['SPDB'] = crawl_spdb(from_date)
    maintain_list['GDB'] = crawl_gdb(from_date)



    #平安银行没找到公告地址
# maintain_list['SZPAB'] = crawl_szpab(from_date)


    # maintain_list['HCCB'] = crawl_hccb(from_date)
    #暂时交易量<100/天
    # maintain_list['BOS'] = crawl_bos(from_date)
    # maintain_list['BCCB'] = crawl_bccb(from_date)
    # maintain_list['CZB'] = crawl_czb(from_date)
    # maintain_list['HKBCHINA'] = crawl_hkbchina(from_date)

    return maintain_list


def need_notify(title, release_date, from_date, bank=None):
    return title is not None and (title.find('维护') > -1 or title.find('暂停') > -1 or title.find('升级') > -1
                                  or title.find('停业') > -1 or title.find('停运') > -1 or title.find('域名') > -1)


def crawl_abc(from_date):
    target_url = r"http://www.abchina.com/cn/PersonalServices/SvcBulletin/"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.details_rightWrapC ul li.cf')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a').text(), format_date_md(pyq(i).find('.details_rightD').text()), from_date,
                       'ABC'):
            maintain = {}
            maintain['url'] = target_url + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = format_date_md(pyq(i).find('.details_rightD').text())
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.details_rightWrapT').text()
            maintain['content'] = detail.find('.TRS_Editor').text()
            maintain_list.append(maintain)

    # print(maintain_list)
    return maintain_list


def crawl_ccb(from_date):
    target_url = r"http://www.ccb.com/cn/v3/include/notice/"
    # result = requests.get(url)
    doc = pyq(url=target_url + 'zxgg_1.html', encoding="utf-8")
    cts = doc('.w_720 ul li')
    maintain_list = []
    for i in cts:
        if (need_notify(pyq(i).find('a').text(), pyq(i).find('span').text(), from_date, 'CCB')):
            maintain = {}
            maintain['url'] = target_url + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = pyq(i).find('span').text()
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.w_660 .content h2.Yahei').text()
            maintain['content'] = detail.find('.w_660 .content #ti').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_boc(from_date):
    target_url = r"http://www.boc.cn/custserv/bi2/"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.main ul.list li')
    maintain_list = []
    for i in cts:
        release_date = pyq(i).find('span').text().replace("[", "").replace("]", "").replace(" ","")
        if (need_notify(pyq(i).find('a').text(), release_date, from_date, 'BOC')):
            maintain = {}
            maintain['url'] = target_url + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = release_date
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.container .content .title').text()
            maintain['content'] = detail.find('.container .content .sub_con').text()
            maintain_list.append(maintain)
    return maintain_list


def crawl_icbc(from_date):
    target_url = r"http://www.icbc.com.cn/ICBC/%E9%87%8D%E8%A6%81%E5%85%AC%E5%91%8A/%E9%87%8D%E8%A6%81%E5%85%AC%E5%91%8A/default.htm"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('#middlebox .box_normal table tr')
    maintain_list = []
    for i in cts:
        if (need_notify(pyq(i).find('td:nth-child(2) a').text(), cn_format(pyq(i).find('td:nth-child(3) a').text()),
                        from_date, 'ICBC')):
            maintain = {}
            maintain['url'] = "http://www.icbc.com.cn/" + pyq(i).find('td:nth-child(2) a').attr("href")
            maintain['title'] = pyq(i).find('td:nth-child(2) a').text()
            maintain['release-date'] = cn_format(pyq(i).find('td:nth-child(3) a').text())
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find(
                '#FreePlaceHoldersControl1 #NCPHRICH_TitleHtmlPlaceholderDefinition').text()
            maintain['content'] = detail.find('#FreePlaceHoldersControl1 #mypagehtmlcontent').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_cmb(from_date):
    target_url = r"http://www.cmbchina.com/main/"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.container .content table tr')
    maintain_list = []
    for i in cts:
        release_date = pyq(i).find('span span').text().replace('[','').replace(']','')
        if need_notify(pyq(i).find('a').text(),release_date , from_date, ''):
            maintain = {}
            maintain['url'] = "http://www.cmbchina.com/" + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = release_date
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.DivContainer .notice h2.head span').text()
            maintain['content'] = detail.find('.DivContainer .notice .infocontainer .infocontent').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_comm(from_date):
    target_url = r"http://www.bankcomm.com/BankCommSite/shtml/jyjr/cn/7158/7825/list_1.shtml?channelId=7158"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.memu-box-list-tzzgx ul.tzzgx-conter li')
    maintain_list = []
    for i in cts:
        release_date = pyq(i).find('span').text().replace('[','').replace(']','')
        if need_notify(pyq(i).find('a').text(),release_date , from_date, ''):
            maintain = {}
            maintain['url'] = "http://www.bankcomm.com" + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = release_date
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.main .news-block h2').text()
            maintain['content'] = detail.find('.main .news-block .show_main.c_content').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_ceb(from_date):
    target_url = r"http://www.cebbank.com/site/zhpd/gdgg10/index.html"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.gg_right ul.gg_right_ul li')
    maintain_list = []
    for i in cts:
        if (need_notify(pyq(i).find('a').text(), pyq(i).find('span.sp2').text(), from_date, 'ICBC')):
            maintain = {}
            maintain['url'] = "http://www.cebbank.com" + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = pyq(i).find('span.sp2').text()
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('#main_con .gd_xilan .title').text()
            maintain['content'] = detail.find('#main_con .gd_xilan .xilan_con').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_psbc(from_date):
    target_url = r"http://www.psbc.com/cn/index/ggl/index.html"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.rightmain .new_list_box .forextab li')
    maintain_list = []
    for i in cts:
        if (need_notify(pyq(i).find('a').text(), pyq(i).find('span').text(), from_date, 'PSBC')):
            maintain = {}
            maintain['url'] = "http://www.psbc.com" + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = pyq(i).find('span').text()
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.rightmain .news_cont_tit h6').text()
            maintain['content'] = detail.find('.rightmain .news_cont_msg').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_citic(from_date):
    target_url = r"http://www.citicbank.com/common/servicenotice/"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.row ul.dhy_b li')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a').text(), pyq(i).find('span').text(), from_date, ''):
            maintain = {}
            maintain['url'] = target_url + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = pyq(i).find('span').text()
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.main_right h1.center').text()
            maintain['content'] = detail.find('.main_right .main_content').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_cmbc(from_date):
    target_url = r"http://www.cmbc.com.cn/cs/Satellite?c=Page&cid=1378263044880&currentId=1356495497180&pagename=cmbc%2FPage%2FTP_AboutMs&rendermode=preview#"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.counter_mid_1 ul.news_list li.left_ul520')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a').text(), pyq(i).find('span.right').text(), from_date, ''):
            maintain = {}
            maintain['url'] = "http://www.cmbc.com.cn" + pyq(i).find('a').attr("href").replace('\t', '').replace('\r',
                                                                                                                 '').replace(
                '\n', '').replace(' ', '')
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = pyq(i).find('span.right').text()
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.counter_mid_1 .PubBox .ms_fl').text()
            maintain['content'] = detail.find('.counter_mid_1 .count_one .count_one').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_cib(from_date):
    target_url = r"http://www.cib.com.cn/cn/aboutCIB/about/notice/"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('#content .list-box ul li.clearfix')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a').text(), pyq(i).find('span').text(), from_date, ''):
            maintain = {}
            maintain['url'] = "http://www.cib.com.cn"+pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = pyq(i).find('span').text()
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('#content .detail-box .middle h1').text()
            maintain['content'] = detail.find('#content .detail-box .middle').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_szpab(from_date):
    target_url = r"http://www.abchina.com/cn/PersonalServices/SvcBulletin/"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.details_rightWrapC ul li.cf')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a').text(), pyq(i).find('span').text(), from_date, ''):
            maintain = {}
            maintain['url'] = target_url + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = format_date_md(pyq(i).find('.details_rightD').text())
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.details_rightWrapT').text()
            maintain['content'] = detail.find('.TRS_Editor').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_hccb(from_date):
    target_url = r"http://www.hzbank.com.cn/hzyh/index/bxgg/index.html"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('#yc_main .new_list1 ul li')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a').text(), pyq(i).find('span:nth-child(2)').text(), from_date, ''):
            maintain = {}
            maintain['url'] = "http://www.hzbank.com.cn" + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = pyq(i).find('span:nth-child(2)').text()
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.easysite-news-peruse .easysite-news-title h2').text()
            maintain['content'] = detail.find('.easysite-news-peruse .easysite-news-content').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_spdb(from_date):
    target_url = r"http://www.spdb.com.cn/home/sygg/"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.c_news_div .c_news_body ul li')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a').text(), pyq(i).find('span').text(), from_date, ''):
            maintain = {}
            maintain['url'] = pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = pyq(i).find('span').text()
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('#main .c_article_title p').text()
            maintain['content'] = detail.find('#main .c_article_body').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_gdb(from_date):
    target_url = r"http://www.cgbchina.com.cn/Channel/11640277"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="gbk")
    cts = doc('.rightContainer .textContent .listContent ul.newList li')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a').text(), pyq(i).find('span').text(), from_date, ''):
            maintain = {}
            maintain['url'] = "http://www.cgbchina.com.cn" + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = pyq(i).find('span').text()
            detail = pyq(url=maintain['url'], encoding="gbk")
            maintain['full-title'] = maintain['title']
            maintain['content'] = detail.find('.mainContent .textContent .MsoNormal').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


# def crawl_hkbchina(from_date):
#     target_url = r"http://www.abchina.com/cn/PersonalServices/SvcBulletin/"
#     # result = requests.get(url)
#     doc = pyq(url=target_url, encoding="utf-8")
#     cts = doc('.details_rightWrapC ul li.cf')
#     maintain_list = []
#     for i in cts:
#         if need_notify(pyq(i).find('a').text(), pyq(i).find('span').text(), from_date, ''):
#             maintain = {}
#             maintain['url'] = target_url + pyq(i).find('a').attr("href")
#             maintain['title'] = pyq(i).find('a').text()
#             maintain['release-date'] = format_date_md(pyq(i).find('.details_rightD').text())
#             detail = pyq(url=maintain['url'], encoding="utf-8")
#             maintain['full-title'] = detail.find('.details_rightWrapT').text()
#             maintain['content'] = detail.find('.TRS_Editor').text()
#             maintain_list.append(maintain)
#     # print(maintain_list)
#     return maintain_list


def crawl_hxb(from_date):
    target_url = r"http://www.hxb.com.cn/home/cn/clientServ/newAnnoun/list.shtml"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.pro_bankinfoList .pro_contlist ul li.pro_contli')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a span.pro_word').text(), pyq(i).find('span.pro_time').text(), from_date, ''):
            maintain = {}
            maintain['url'] =  pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a span.pro_word').text()
            maintain['release-date'] = pyq(i).find('span.pro_time').text()
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('#pro_contp_ .Contentstitle').text()
            maintain['content'] = detail.find('#content').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_bos(from_date):
    target_url = r"http://www.abchina.com/cn/PersonalServices/SvcBulletin/"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.details_rightWrapC ul li.cf')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a').text(), pyq(i).find('span').text(), from_date, ''):
            maintain = {}
            maintain['url'] = target_url + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = format_date_md(pyq(i).find('.details_rightD').text())
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.details_rightWrapT').text()
            maintain['content'] = detail.find('.TRS_Editor').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_bccb(from_date):
    target_url = r"http://www.abchina.com/cn/PersonalServices/SvcBulletin/"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.details_rightWrapC ul li.cf')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a').text(), pyq(i).find('span').text(), from_date, ''):
            maintain = {}
            maintain['url'] = target_url + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = format_date_md(pyq(i).find('.details_rightD').text())
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.details_rightWrapT').text()
            maintain['content'] = detail.find('.TRS_Editor').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


def crawl_czb(from_date):
    target_url = r"http://www.abchina.com/cn/PersonalServices/SvcBulletin/"
    # result = requests.get(url)
    doc = pyq(url=target_url, encoding="utf-8")
    cts = doc('.details_rightWrapC ul li.cf')
    maintain_list = []
    for i in cts:
        if need_notify(pyq(i).find('a').text(), pyq(i).find('span').text(), from_date, ''):
            maintain = {}
            maintain['url'] = target_url + pyq(i).find('a').attr("href")
            maintain['title'] = pyq(i).find('a').text()
            maintain['release-date'] = format_date_md(pyq(i).find('.details_rightD').text())
            detail = pyq(url=maintain['url'], encoding="utf-8")
            maintain['full-title'] = detail.find('.details_rightWrapT').text()
            maintain['content'] = detail.find('.TRS_Editor').text()
            maintain_list.append(maintain)
    # print(maintain_list)
    return maintain_list


"mm-dd"


def format_date_md(mm_dd):
    if len(mm_dd) < 2:
        return mm_dd
    month = mm_dd[0:2]
    now = datetime.datetime.now()
    if int(month) > 10 and now.month < 3:
        return str(now.year - 1) + '-' + mm_dd
    return str(now.year) + '-' + mm_dd


def cn_format(mm_dd):
    if mm_dd is None:
        return None
    return mm_dd.replace("年", "-").replace("月", "-").replace("日", "-")


if __name__ == '__main__':
    content = "四、客户端登录 “中信投资”交易平台上线后，“汇金宝”存量开立手机银行客户（“汇金宝“保证金专户余额大于 0 ）可使用手机银行用户直接登录”中信投资“交易平台；没有注册我行手机银行的客户，可通过“中信投资” APP 注册用户并绑定原“汇金宝”签约卡。其它客户欢迎您通过手机 APP 注册新用户后使用“中信投资”交易平台进行个人外汇、贵金属买卖交易。 由此给您带来不便，敬请谅解。如有疑问，请致电我行客服中心 95558 或咨询当地中信银行营业网点。 感谢您一直以来对我行个人外汇、纸黄金买卖业务的关注与支持！ 特此公告"
    send_mail('银行维护提醒', content, 'dragonsmaug@126.com',
        ['out_lier@126.com'], fail_silently=False)

    # print(format_date_md("12-11"))
