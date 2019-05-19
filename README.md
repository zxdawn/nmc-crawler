# nmc-crawler
## What is it?

Script of downloading figures from NMC website: http://www.nmc.cn/

Now, this script supports downloading **weathercharts** and **radar** figures.

## Usage

Download or clone the repository first

```
git clone https://github.com/zxdawn/nmc-crawler.git
```

Check the help information

```
python nmc_crawler.py --help
```
```
Usage: nmc_crawler.py [OPTIONS]

  Download weathercharts and radar figures from NMC.
  Contact:
      xinzhang1215@gmail.com

Options:
  -k, --kind [radar|weatherchart]
                                  Kind of data  [required]
  -a, --area [all|regions|stations]
                                  Region of maps: 
                                  For weatherchart, you don't
                                  need to specify this parameter.  [default:
                                  regions]
  -r, --resolution [medium|small]
                                  Resolution of figures  [default: medium]
  -s, --savepath TEXT             Savepath of figures  [default: ./]
  -v, --verbose INTEGER           verbose level  [default: 0]
  --help                          Show this message and exit.

```

## Brief example

1. Download regional radar figures:

![radar_1](<https://github.com/zxdawn/nmc-crawler/raw/master/examples/radar_1.gif)

2. Download radar figures of all stations:

   ![radar_2](<https://github.com/zxdawn/nmc-crawler/raw/master/examples/radar_2.gif)

3. Download weathercharts:

   ![weatherchart](<https://github.com/zxdawn/nmc-crawler/raw/master/examples/weatherchart.gif)