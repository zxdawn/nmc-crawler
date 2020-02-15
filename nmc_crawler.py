import os
import click
import time
import requests
import argparse
import urllib.error
import urllib.request
from bs4 import BeautifulSoup

domain_name = 'http://www.nmc.cn'
base_mosaic_url = domain_name + '/publish/radar/chinaall.html'
base_station_url = domain_name + '/publish/radar/bei-jing/da-xing.htm'
base_wc_url = domain_name + '/publish/observations/china/dm/weatherchart-h000.htm'
base_ltng_url = domain_name + '/publish/observations/lighting.html'

# Get all urls
class NMC(object):
    def __init__(self, kind, area, resolution, savepath, verbose):
        self.kind = kind
        self.area = area
        self.resolution = resolution
        self.savepath = savepath
        self.verbose = verbose

        if self.area == 'region':
            self.suffix = 'html'
            self.base_url = base_mosaic_url

        elif self.area == 'station':
            self.suffix = 'htm'
            self.base_url = base_station_url

        elif self.area == 'china':
            if self.kind == 'ltng':
                self.base_url = base_ltng_url
                self.suffix = 'html'
            elif self.kind == 'weatherchart':
                self.base_url = base_wc_url
                self.suffix = 'htm'

    def get_urls(self):
    # Get urls
        htmls = []
        while htmls == []:
            try:
                base_page = requests.get(self.base_url)
                soup = BeautifulSoup(base_page.content, 'html.parser')
                for link in soup.findAll('a'):
                    sub_urls = link.get('href')
                    if self.kind == 'radar':
                        if sub_urls.startswith('/publish/radar/') & sub_urls.endswith(self.suffix):
                            htmls.append(sub_urls)
                    elif self.kind == 'weatherchart':
                        if sub_urls.startswith('/publish/observations/china/dm/weatherchart') & sub_urls.endswith(self.suffix):
                            htmls.append(sub_urls)
                    elif self.kind == 'ltng':
                        if sub_urls.startswith('/publish/observations/lighting') & sub_urls.endswith(self.suffix):
                            htmls.append(sub_urls)
            except:
                self.sleep_message('get_main_url')

        main_url = ['{}{}'.format(domain_name,html) for html in list(set(htmls))]

        if self.kind == 'ltng' or self.area == 'region':
            return main_url
        else:
            urls = []
            for url in main_url:
                urls.extend(self.get_sub_url(url))

            return urls

    def get_sub_url(self, url):
        htmls = []
        while htmls == []:
            try:
                base_page = requests.get(url)
                soup = BeautifulSoup(base_page.content, 'html.parser')
                for link in soup.findAll('a'):
                    sub_htmls = link.get('href')
                    if self.kind == 'radar':
                        if sub_htmls.startswith('/publish/radar/') & sub_htmls.endswith(self.suffix):
                            # Filter out Surpluses
                            if sub_htmls.split("/")[3] == url.split("/")[5]:
                                htmls.append(sub_htmls)
                    elif self.kind == 'weatherchart':
                        if sub_htmls.startswith('/publish/observations/') & sub_htmls.endswith(url[-8:]):
                            if sub_htmls.split("/")[3] == url.split("/")[5]:
                                htmls.append(sub_htmls)                    
            except:
                self.sleep_message('get_sub_url')

        return ['{}{}'.format(domain_name,html) for html in list(set(htmls))]

    def download(self, urls):
        # Download images to savepath
        savepath = os.path.join(self.savepath, self.kind, self.area)

        for url in urls:
            try:
                htmls = self.get_img_urls(url)

                # get dir_name and subdir_name
                if self.area == 'region':
                    dir_name = url.split("/")[5][:-5]
                    subdir_name = ''
                elif self.area == 'station':
                    dir_name = url.split("/")[5]
                    subdir_name = url.split("/")[6][:-4]
                elif self.area == 'china':
                    dir_name = ''
                    subdir_name = url.split("/")[-1][:-4].replace(".", "")

                if self.area == 'region':
                    print ('    Downloading', dir_name, 'mosaics')
                elif self.area == 'station':# and self.verbose > 0:
                    print ('    Downloading', subdir_name, 'mosaics')
                elif self.area == 'china':# and self.verbose > 0:
                    print ('    Downloading', subdir_name)

                # get name/url and download
                for html in htmls:
                    # get date for img_name
                    split_html = html.split("/")
                    date = ''.join(split_html[4:7])
                    if self.kind == 'ltng' or dir_name == 'chinaall' or self.area == 'china':
                        sdate = split_html[9].find(date)
                        edate = sdate + 12
                        name  = split_html[9][sdate:edate]
                    else:
                        sdate = split_html[8].find(date)
                        edate = sdate + 12
                        name  = split_html[8][sdate:edate]

                    # Check whether dirs of savepath exists. If not, create it.
                    if self.kind == 'radar':
                        full_savepath = os.path.join(savepath, dir_name, subdir_name, date[:-2], date[-4:])
                    elif self.kind in ['weatherchart', 'ltng']:
                        full_savepath = os.path.join(savepath, dir_name, date[:-2], subdir_name)

                    if not os.path.exists(full_savepath):
                        if self.verbose > 0:
                            print ('mkdir ' + full_savepath)
                        os.makedirs(full_savepath, exist_ok=True)

                    if self.kind == 'radar':
                        fullfilename = os.path.join(full_savepath, name + '.png')
                    else:
                        fullfilename = os.path.join(full_savepath, name + '.jpg')

                    if os.path.isfile(fullfilename):
                        if self.verbose > 0:
                            print ('    ', name, 'exists in', full_savepath, ' Skip!!')
                    else:
                        urllib.request.urlretrieve(html, fullfilename)
                        if self.verbose > 0:
                            print ('        Downloading',name)

            except urllib.error.HTTPError as err:
                # pass
                print(err.code)

            finally:
                finish_output = '    Finish. Save images to ' + os.path.join(savepath,dir_name)
                if self.area == 'region':
                    print (finish_output)
        
        if self.area == 'station':
            print (finish_output)

    def get_img_urls(self, url):
        page = ''
        while page == '':
            try:
                # Download the Response object and parse
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')

                # Finding all instances of 'img' at once
                pics = soup.find_all('p', class_='img')

                # get url of each picture and save to a list
                img_urls = []
                for pic in pics:
                    img_url = pic.img.get('data-original')
                    img_urls.append(img_url)
                img_urls = [url.replace('small', self.resolution) for url in img_urls]
            except:
                self.sleep_message('get_img_urls')

        return img_urls

    def sleep_message(self, func_name):
        print('Connection of ' + func_name + ' refused by the server..')
        print('Let me sleep for 5 seconds')
        print('ZZzzzz...')
        time.sleep(5)

# -------------------------------------------------------
@click.command()
@click.option(
    '--kind',
    '-k',
    type=click.Choice(['radar', 'weatherchart', 'ltng']),
    help='Kind of data',
    required=True
)

@click.option(
    '--area',
    '-a',
    default = 'region',
    type=click.Choice(['all', 'region','station']),
    help='''
    Region of maps: 
    For weatherchart and ltng, you don't
    need to specify this parameter.
    ''',
    show_default=True
)

@click.option(
    '--resolution',
    '-r',
    default = 'medium',
    type=click.Choice(['medium', 'small']),
    help='Resolution of figures',
    show_default=True
)

@click.option(
    '--savepath',
    '-s',
    default = './',
    help='Savepath of figures',
    show_default=True
)

@click.option(
    '--verbose',
    '-v',
    default = 0,
    help='verbose level',
    show_default=True
)
# -------------------------------------------------------

def main(kind, area, resolution, savepath, verbose):
    '''
    \b
    Download weathercharts and radar figures from NMC.
    Contact:
        xinzhang1215@gmail.com
    '''
    s = requests.session()
    s.keep_alive = False

    if kind == 'radar':
        # refresh log file
        f = open('radar.log', 'w+')
        f.truncate(0)

        # download radar mosaics
        if area == 'all':
            nmc = NMC(kind, 'region', resolution, savepath, verbose)
            all_urls = nmc.get_urls()
            nmc.download(all_urls)

            nmc = NMC(kind, 'station', resolution, savepath, verbose)
            all_urls = nmc.get_urls()
            nmc.download(all_urls)

        elif area in ['region', 'station']:
            nmc = NMC(kind, area, resolution, savepath, verbose)
            all_urls = nmc.get_urls()
            nmc.download(all_urls)

    elif kind == 'weatherchart':
        # refresh log file
        f = open('weatherchart.log', 'w+')
        f.truncate(0)

        # download weathercharts
        nmc = NMC(kind, 'china', resolution, savepath, verbose)
        all_urls = nmc.get_urls()
        nmc.download(all_urls)

    elif kind == 'ltng':
        # refresh log file
        f = open('lightning.log', 'w+')
        f.truncate(0)

        # download weathercharts
        nmc = NMC(kind, 'china', resolution, savepath, verbose)
        all_urls = nmc.get_urls()
        nmc.download(all_urls)

if __name__ == '__main__':
    start_time = time.time()
    main()
    # print("--- %s seconds ---" % (time.time() - start_time))
