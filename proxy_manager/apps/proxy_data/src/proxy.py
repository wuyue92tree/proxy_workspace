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
        self.q = RedisQueue('proxy_task', host=REDIS_HOST, port=REDIS_PORT,
                            password=REDIS_PASSWORD)

    def format_level(self, level):
        if level == '透明':
            return 1
        elif level == '高匿':
            return 2

    def format_type(self, type):
        if type.upper() == 'HTTP':
            return 1
        elif type.upper() == 'HTTPS':
            return 2
        else:
            # type = 'HTTP/HTTPS'
            return 3

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
                    level = self.format_level(level)
                    type = soup.find_all('td')[5].text.encode('utf-8')
                    type = self.format_type(type)
                    live_time = soup.find_all('td')[8].text.encode('utf-8')
                    dateline = datetime.datetime.now()
                    self.logger.info('%s\t%s\t%s\t%s\t%s\t%s\t%s'
                                     % (addr, port, locate, level,
                                        type, live_time, dateline))

                    data.append({
                        'addr': addr,
                        'port': port,
                        'locate': locate.decode('utf-8'),
                        'level': level,
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

            self.logger.info('crawler finish from xici!!!')

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
                    level = self.format_level(level)
                    type = soup.find_all('td')[3].text.encode('utf-8')
                    type = self.format_type(type)
                    dateline = datetime.datetime.now()
                    self.logger.info('%s\t%s\t%s\t%s\t%s\t%s'
                                     % (addr, port, locate,
                                        level, type, dateline))
                    data.append({
                        'addr': addr,
                        'port': port,
                        'locate': locate.decode('utf-8'),
                        'level': level,
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

            self.logger.info('crawler finish from kuai!!!')

        except Exception as e:
            self.logger.exception('you got a error %s' % e)

    def create_task(self):
        try:
            if not self.q.empty():
                self.q.clean()
                self.logger.info("清空任务队列.")

            sites = self.db.session.query(ProxyDataTargetsite).filter_by(
                status=True).all()

            for site in sites:
                domains = self.db.session.query(ProxyDataCheckdomain).filter_by(
                    site_id=site.id, status=True)

                for domain_item in domains:
                    check_url = domain_item.check_url
                    domain = domain_item.domain
                    domain_id = domain_item.id

                    proxys = self.db.session.query(ProxyDataProxy)
                    for proxy_item in proxys:
                        proxy_id = proxy_item.id
                        proxy = proxy_item.addr + ':' + proxy_item.port
                        self.q.put((domain_id, domain, check_url, proxy_id,
                                    proxy))
                        # print(domain_id, domain, check_url, proxy_id,
                        #       proxy)
            self.logger.info("总计生成%s个任务。" % self.q.qsize())

        except Exception as e:
            self.logger.exception(e)

    def check(self):
        while 1:
            try:
                if not self.q.empty():
                    domain_id, domain, check_url, proxy_id, proxy = eval(
                        self.q.get())
                    proxies = {
                        'http': 'http://%s' % proxy,
                        'https': 'http://%s' % proxy,
                    }

                    try:
                        res = self.html_downloader.download(check_url,
                                                            proxies=proxies,
                                                            timeout=5)
                    except requests.RequestException:
                        self.logger.warning("代理检测失败：domain->%s proxy->%s\t%s"
                                            % (domain.encode('utf-8'),
                                               proxy.encode('utf-8'),
                                               self.q.qsize()))
                        continue
                    connect_time = res.elapsed.microseconds * 0.0000001
                    check_time = datetime.datetime.now()
                    # self.logger.info('%s\t%s\t%s\t%s\t%s'
                    #                  % (domain_id, proxy_id, proxy,
                    #                     connect_time,
                    #                     self.q.qsize()))
                    item = ProxyDataProxychecked(proxy_id=proxy_id,
                                                 domain_id=domain_id,
                                                 connect_time=connect_time,
                                                 check_time=check_time)
                    try:
                        self.db.session.add(item)
                        self.db.session.commit()
                    except:
                        update_ = {}
                        update_['connect_time'] = connect_time
                        update_['check_time'] = check_time
                        self.db.session.rollback()
                        self.db.session.query(ProxyDataProxychecked).filter_by(
                            proxy_id=proxy_id, domain_id=domain_id).update(
                            update_)
                        self.db.session.commit()
                    self.logger.info("代理检测成功: domain->%s proxy->%s\t%s"
                                     % (domain.encode('utf-8'),
                                        proxy.encode('utf-8'),
                                        self.q.qsize()))
            except Exception as e:
                self.logger.exception(e)

    def run(self):
        try:
            worker = sys.argv[4]
        except IndexError:
            print('No worker found !\n')
            sys.exit()

        if worker == 'get_xici':
            self.crawler_xicidaili('http://www.xicidaili.com/nn/', io=1)
            self.crawler_xicidaili('http://www.xicidaili.com/nt/', io=1)
            self.crawler_xicidaili('http://www.xicidaili.com/wn/', io=1)
            self.crawler_xicidaili('http://www.xicidaili.com/wt/', io=1)

        elif worker == 'get_kuai':
            self.crawler_kuaidaili('http://www.kuaidaili.com/free/inha/', io=1)
            self.crawler_kuaidaili('http://www.kuaidaili.com/free/intr/', io=1)
            self.crawler_kuaidaili('http://www.kuaidaili.com/free/outha/',
                                   io=2)
            self.crawler_kuaidaili('http://www.kuaidaili.com/free/outtr/',
                                   io=2)

        elif worker == 'create_task':
            self.create_task()

        elif worker == 'check':
            self.check()

        else:
            print('"%s" is not a valid worker!' % worker)
            sys.exit()
