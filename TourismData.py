from XC.xiechen import XCCrawler
import DB.sql as sql
import CONFIG

place = sql.buildMainData(CONFIG.PLACE)
xc = XCCrawler(place)
