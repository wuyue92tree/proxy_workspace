#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# author: wuyue92tree@163.com


from __future__ import print_function

import datetime
import time
import sys
import requests
from crwy.spider import Spider
from crwy.utils.queue.RedisQueue import RedisQueue
from crwy.utils.logger import Logger
from crwy.utils.sql.db import Database
from proxy_db import *

REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PASSWORD = ''

page_num = 6
process_num = 10


class ProxySpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.spider_name = 'proxy'
        self.logger = Logger.rt_logger()
        self.db = Database('sqlite:///../../../db.sqlite3',
                           encoding='utf-8')
        self.db.init_table()

    def crawler_xicidaili(self, target_url, io):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/'
                              '537.36 (KHTML, like Gecko)'
                              'Chrome/59.0.3071.109  Safari/537.36',
                'Host': 'www.xicidaili.com'
            }
            for i in range(1, page_num):
                url = target_url + str(i)
                try:
                    res = self.html_downloader.download(url, headers=headers)
                    html_cont = res.content
                except requests.RequestException:
                    self.logger.warning('fail to access %s' % url)
                    continue
                try:
                    soups = self.html_parser.parser(html_cont).find_all(
                        'tr', class_='odd')
                except AttributeError:
                    self.logger.warning('analysis fail on %s' % url)
                    continue

                if not soups:
                    self.logger.warning("no proxy founded: %s" % url)
                    continue

                data = []
                for soup in soups:
                    addr = soup.find_all('td')[1].text.encode('utf-8')
                    port = soup.find_all('td')[2].text.encode('utf-8')
                    locate = soup.find_all('td')[3].text.strip().encode(
                        'utf-8')
                    level = soup.find_all('td')[4].text.encode('utf-8')
                    type = soup.find_all('td')[5].text.encode('utf-8')
                    live_time = soup.find_all('td')[8].text.encode('utf-8')
                    dateline = datetime.datetime.now()
                    self.logger.info('%s\t%s\t%s\t%s\t%s\t%s\t%s'
                                     % (addr, port, locate, level,
                                        type, live_time, dateline))

                    data.append({
                        'addr': addr,
                        'port': port,
                        'locate': locate.decode('utf-8'),
                        'level': level.decode('utf-8'),
                        'type': type,
                        'io': io,
                        'live_time': live_time.decode('utf-8'),
                        'dateline': dateline,
                        'source': u'西刺代理'
                    })
                self.db.session.execute(
                    ProxyDataProxy.__table__.insert().prefix_with("OR "
                                                                  "REPLACE"),
                    data
                )
                self.db.session.commit()

            self.logger.info('crawler finish %s!!!' % url)

        except Exception as e:
            self.logger.exception('you got a error %s' % e)

    def crawler_kuaidaili(self, target_url, io):
        try:
            for i in range(1, page_num):
                time.sleep(2)
                url = target_url + str(i)
                try:
                    res = self.html_downloader.download(url)
                    html_cont = res.content
                except requests.RequestException:
                    self.logger.warning('fail to access %s' % url)
                    continue
                try:
                    soups = self.html_parser.parser(
                        html_cont).find('tbody').find_all('tr')
                except AttributeError:
                    self.logger.warning('analysis fail on %s' % url)
                    continue

                if not soups:
                    self.logger.warning("no proxy founded: %s" % url)
                    continue

                data = []
                for soup in soups:
                    addr = soup.find_all('td')[0].text.encode('utf-8')
                    port = soup.find_all('td')[1].text.encode('utf-8')
                    locate = soup.find_all('td')[4].text.strip().encode(
                        'utf-8')
                    level = soup.find_all('td')[2].text.encode('utf-8').strip(
                        '名')
                    type = soup.find_all('td')[3].text.encode('utf-8')
                    dateline = datetime.datetime.now()
                    self.logger.info('%s\t%s\t%s\t%s\t%s\t%s'
                                     % (addr, port, locate,
                                        level, type, dateline))
                    data.append({
                        'addr': addr,
                        'port': port,
                        'locate': locate.decode('utf-8'),
                        'level': level.decode('utf-8'),
                        'type': type,
                        'io': io,
                        'dateline': dateline,
                        'source': u'快代理'
                    })
                self.db.session.execute(
                    ProxyDataProxy.__table__.insert().prefix_with("OR "
                                                                  "REPLACE"),
                    data
                )
                self.db.session.commit()

            self.logger.info('crawler finish !!!')

        except Exception as e:
            self.logger.exception('you got a error %s' % e)

    # def check(self, q, site):
    #     while True:
    #         if q.empty():
    #             print('check queue is Empty!!! have fun.')
    #             exit()
    #         site_id = site.id
    #         url = site.site
    #         proxy_id, addr, port, type = eval(q.get())
    #         proxy = [addr + ':' + port]
    #
    #         try:
    #             res = self.html_downloader.download(url, proxy=proxy)
    #         except pycurl.error:
    #             # self.logger.warning('%s: fail to access %s by %s %s'
    #             #                     % (get_current_function_name(), url,
    #             #                        proxy[0], q.qsize()))
    #             continue
    #         connect_time = float(res.http_conn_time)
    #         connect_time = format(connect_time, '.6f')
    #         check_time = datetime.datetime.now()
    #         # print(check_time)
    #         self.logger.info('%s\t%s\t%s\t%s'
    #                          % (site_id, proxy[0], connect_time, q.qsize()))
    #
    #         item = ProxyProxychecked(proxy_id=proxy_id, site_id=site_id,
    #                                  connect_time=connect_time,
    #                                  check_time=check_time)
    #         try:
    #             self.db.session.add(item)
    #             self.db.session.commit()
    #         except:
    #             update_ = {}
    #             update_['connect_time'] = connect_time
    #             update_['check_time'] = check_time
    #             self.db.session.rollback()
    #             self.db.session.query(ProxyProxychecked).filter_by(proxy_id=proxy_id, site_id=site_id).update(update_)
    #             self.db.session.commit()
    #
    # def do_check(self):
    #     process_list = []
    #     sites = self.db.session.query(ProxyTargetsite).filter_by(status=1)
    #     if not sites:
    #         print('No active checking site found!\n')
    #         exit()
    #
    #     for i in range(process_num):
    #         for site in sites:
    #             p = multiprocessing.Process(target=self.check,
    #                                         args=(self.q_check(site.id), site))
    #             process_list.append(p)
    #             p.start()
    #
    #     for p in process_list:
    #         p.join()
    #
    # def q_check(self, site_id):
    #     res = self.db.session.query(ProxyProxy).all()
    #
    #     q = RedisQueue(
    #         'proxy'+str(site_id),
    #         host=REDIS_HOST,
    #         port=REDIS_PORT,
    #         password=REDIS_PASSWORD
    #     )
    #     if q.empty():
    #         for i in res:
    #             q.put((i.id, i.addr, i.port, i.type))
    #
    #     return q

    def run(self):
        try:
            worker = sys.argv[4]
        except IndexError:
            print('No worker found !\n')
            sys.exit()

        if worker == 'xici':
            self.crawler_xicidaili('http://www.xicidaili.com/nn/', io=1)
            self.crawler_xicidaili('http://www.xicidaili.com/nt/', io=1)
            self.crawler_xicidaili('http://www.xicidaili.com/wn/', io=1)
            self.crawler_xicidaili('http://www.xicidaili.com/wt/', io=1)

        elif worker == 'kuai':
            self.crawler_kuaidaili('http://www.kuaidaili.com/free/inha/', io=1)
            self.crawler_kuaidaili('http://www.kuaidaili.com/free/intr/', io=1)
            self.crawler_kuaidaili('http://www.kuaidaili.com/free/outha/',
                                   io=2)
            self.crawler_kuaidaili('http://www.kuaidaili.com/free/outtr/',
                                   io=2)

        # elif worker == 'check':
        #     self.do_check()

        else:
            print('"%s" is not a valid worker!' % worker)
            sys.exit()
