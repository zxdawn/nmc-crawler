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
base_obs_url = domain_name + '/publish/observations/china/dm/weatherchart-h000.htm'

def sleep_message(func_name):
    print('Connection of ' + func_name + ' refused by the server..')
    print('Let me sleep for 5 seconds')
    print('ZZzzzz...')
    sleep(5)

# Get main urls
def get_main_url(kind, base_url, suffix):
    htmls = []
    while htmls == []:
        try:
            base_page = requests.get(base_url)
            soup = BeautifulSoup(base_page.content, 'html.parser')
            for link in soup.findAll('a'):
                sub_htmls = link.get('href')
                if kind == 'radar':
                    if sub_htmls.startswith('/publish/radar/') & sub_htmls.endswith(suffix):
                        htmls.append(sub_htmls)
                elif kind == 'weatherchart':
                    if sub_htmls.startswith('/publish/observations/china/dm/weatherchart') & sub_htmls.endswith(suffix):
                        htmls.append(sub_htmls)
        except:
            sleep_message('main_url')

    return ['{}{}'.format(domain_name,html) for html in list(set(htmls))]

def get_sub_url(kind, base_url, suffix):
    htmls = []
    while htmls == []:
        try:
            base_page = requests.get(base_url)
            soup = BeautifulSoup(base_page.content, 'html.parser')
            for link in soup.findAll('a'):
                sub_htmls = link.get('href')
                if kind == 'radar':
                    if sub_htmls.startswith('/publish/radar/') & sub_htmls.endswith(suffix):
                        # Filter out Surpluses
                        if sub_htmls.split("/")[3] == base_url.split("/")[5]:
                            htmls.append(sub_htmls)
                elif kind == 'weatherchart':
                    if sub_htmls.startswith('/publish/observations/') & sub_htmls.endswith(base_url[-8:]):
                        # Filter out Surpluses
                        if sub_htmls.split("/")[3] == base_url.split("/")[5]:
                            htmls.append(sub_htmls)                    
        except:
            sleep_message('station_url')

    return ['{}{}'.format(domain_name,html) for html in list(set(htmls))]

def get_img_urls(url, resolution):
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
            img_urls = [url.replace('small', resolution) for url in img_urls]
        except:
            sleep_message('img_urls')

    return img_urls

def download(urls, kind, region, resolution, savepath, debug):
    # Download images to savepath
    savepath = os.path.join(savepath, kind, region)
    if region == 'region':
        print ('Downloading regional radar maps......')
    elif region == 'station':
        print ('Downloading ' + urls[0].split("/")[5] + ' radar maps......')
    elif region == 'china':
        print ('Downloading China ' + urls[0].split("/")[-1][0:-4] + ' weatherchart ......')

    for url in urls:
        try:
            htmls = get_img_urls(url, resolution)

            # get dir_name and subdir_name
            if region == 'region':
                dir_name = url.split("/")[5][:-5]
                subdir_name = ''
            elif region == 'station':
                dir_name = url.split("/")[5]
                subdir_name = url.split("/")[6][:-4]
            elif region == 'china':
                dir_name = ''
                subdir_name = url.split("/")[-1][:-4]

            if region == 'region':
                print ('    Downloading', dir_name, 'mosaics')
            elif region == 'station' and debug > 0:
                print ('    Downloading', subdir_name, 'mosaics')
            elif region == 'china' and debug > 0:
                print ('    Downloading', subdir_name)

            # get name/url and download
            for html in htmls:
                # get date for img_name
                split_html = html.split("/")
                date = ''.join(split_html[4:7])
                sdate = split_html[9].find(date)
                edate = sdate + 12
                name  = split_html[9][sdate:edate]

                # Check whether dirs of savepath exists. If not, create it.
                if kind == 'radar':
                    full_savepath = os.path.join(savepath, dir_name, subdir_name, date[:-2], date[-4:])
                elif kind == 'weatherchart':
                    full_savepath = os.path.join(savepath, dir_name, date[:-2], subdir_name)

                if not os.path.exists(full_savepath):
                    if debug > 0:
                        print ('mkdir ' + full_savepath)
                    os.makedirs(full_savepath, exist_ok=True)

                if kind == 'radar':
                    fullfilename = os.path.join(full_savepath, name + '.png')
                else:
                    fullfilename = os.path.join(full_savepath, name + '.jpg')

                if os.path.isfile(fullfilename):
                    if debug > 0:
                        print ('    ', name, 'exists in', full_savepath, ' Skip!!')
                else:
                    urllib.request.urlretrieve(html, fullfilename)
                    if debug > 0:
                        print ('        Downloading',name)
                
        except urllib.error.HTTPError as err:
            # pass
            print(err.code)

        finally:
            finish_output = '    Finish. Save images to ' + os.path.join(savepath,dir_name)
            if region == 'region':
                print (finish_output)
    
    if region == 'station':
        print (finish_output)

# Get all urls
def download_imgs(kind, region, resolution, savepath, debug):
    # get main urls;
    # for region: url of areas, suffix = html
    # for station: url of provinces, suffix = htm
    # for weatherchart: url of china, suffix = htm
    if region == 'region':
        suffix = 'html'
        main_htmls = get_main_url(kind, base_mosaic_url, suffix)

    elif region == 'station':
        suffix = 'htm'
        main_htmls = get_main_url(kind, base_station_url, suffix)

    elif region == 'china':
        suffix = 'htm'
        main_obs_htmls = get_main_url(kind, base_obs_url, suffix)

    # for mosaics: download directly
    if region == 'region':
        download (main_htmls, kind, region, resolution, savepath, debug)

    # for station: get urls of sub_station and download
    elif region == 'station':
        for html in main_htmls:
            sub_htmls = get_sub_url(kind, html, suffix)
            download (sub_htmls, kind, region, resolution, savepath, debug)

    # for weatherchart: get urls of sub_urls and download
    elif region == 'china':
        for html in main_obs_htmls:
            sub_htmls = get_sub_url(kind, html, suffix)
            download (sub_htmls, kind, region, resolution, savepath, debug)

# -------------------------------------------------------
@click.command()
@click.option(
    '--kind',
    '-k',
    type=click.Choice(['radar', 'weatherchart']),
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
    For weatherchart, you don't
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
        if area == 'all':
            download_imgs(kind, 'region', resolution, savepath, verbose)
            download_imgs(kind, 'station', resolution, savepath, verbose)
        elif area == 'region' or area == 'station':
            download_imgs(kind, area, resolution, savepath, verbose)

    elif kind == 'weatherchart':
        download_imgs(kind, 'china', resolution, savepath, verbose)


if __name__ == '__main__':
    start_time = time.time()
    main()
    # print("--- %s seconds ---" % (time.time() - start_time))