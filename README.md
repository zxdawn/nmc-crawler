# nmc-crawler
## What is it?

Script of downloading figures from NMC website: http://www.nmc.cn/

Currently, this script supports downloading **weathercharts** and **radar** figures.

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
  -a, --area [all|region|station]
                                  Region of maps: 
                                  For weatherchart, you don't
                                  need to specify this parameter.  [default:
                                  region]
  -r, --resolution [medium|small]
                                  Resolution of figures  [default: medium]
  -s, --savepath TEXT             Savepath of figures  [default: ./]
  -v, --verbose INTEGER           verbose level  [default: 0]
  --help                          Show this message and exit.
```

## Brief example

1. Download regional radar figures:

![radar_1](https://github.com/zxdawn/nmc-crawler/raw/master/examples/radar_1.gif)

2. Download radar figures of all stations:

   ![radar_2](https://github.com/zxdawn/nmc-crawler/raw/master/examples/radar_2.gif)

3. Download weathercharts:

   ![weatherchart](https://github.com/zxdawn/nmc-crawler/raw/master/examples/weatherchart.gif)

## Directory structure

```
├── radar
│   ├── region
│   │   ├── chinaall
│   │   │   └── yyymm
│   │   │       └── mmdd
│   │   ├── dongbei
│   │   │   └── yyymm
│   │   │       └── mmdd
│   │   ├── huabei
│   │   │   └── yyymm
│   │   │       └── mmdd
│   │   ├── huadong
│   │   │   └── yyymm
│   │   │       └── mmdd
│   │   ├── huanan
│   │   │   └── yyymm
│   │   │       └── mmdd
│   │   ├── huazhong
│   │   │   └── yyymm
│   │   │       └── mmdd
│   │   ├── xibei
│   │   │   └── yyymm
│   │   │       └── mmdd
│   │   └── xinan
│   │       └── yyymm
│   │           └── mmdd
│   └── station
│       ├── jiang-su
│       │   ├── chang-zhou
│       │   ├── huai-an
│       │   ├── lian-yun-gang
│       │   ├── nan-jing
│       │   ├── nan-tong
│       │   ├── tai-zhou
│       │   ├── xu-zhou
│       │   └── yan-cheng
│       ├── liao-ning
│       │   ├── chao-yang
│       │   ├── da-lian
│       │   ├── shen-yang
│       │   └── ying-kou
│       └── ....
├── README.md
└── weatherchart
    └── china
        └── yyymm
            ├── cloud-h000
            ├── cloud-h100
            ├── cloud-h200
            ├── cloud-h500
            ├── cloud-h700
            ├── cloud-h850
            ├── cloud-h925
            ├── radar-h000
            ├── radar-h100
            ├── radar-h200
            ├── radar-h500
            ├── radar-h700
            ├── radar-h850
            ├── radar-h925
            ├── weatherchart-h000
            ├── weatherchart-h100
            ├── weatherchart-h200
            ├── weatherchart-h500
            ├── weatherchart-h700
            ├── weatherchart-h850
            └── weatherchart-h925
```