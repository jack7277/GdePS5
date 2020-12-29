from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import re
import threading
import demoji
import emoji as emoji
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram import ParseMode
from LOGGER import Logger


def start(update: Update, context: CallbackContext) -> None:
    # checkStores(update, context)
    pass

def give_emoji_free_text(text):
    return emoji.get_emoji_regexp().sub(r'', text.decode('utf8'))

pat = '^.*<.*>(.*?)<.*>'
def get_text_by_selector(rawHTML, selector):
    try:
        bs = BeautifulSoup(rawHTML, 'html.parser')
        text = str(bs.select(selector)[0])
        status = re.search(pat, text).group(1)
        return status
    except Exception as err:
        return 'Ошибка'


def getTreeByXpath(url, xpath):
    options = FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(15)
    driver.get(url)
    timeout = 30
    try:
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
        content = driver.page_source
        from lxml import html
        tree = html.fromstring(content)
        driver.close()
        driver.quit()
        return content, tree
    finally:
        try:
            driver.close()
            driver.quit()
        except:
            pass

def getTreeByXpath2(url, xpath):
    options = FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(20)
    driver.get(url)
    timeout = 30
    try:
        element_present = EC.text_to_be_present_in_element(By.CSS_SELECTOR, r'#js-product-tile-list > div > div:nth-child(1) > div.fl-product-tile__description.c-product-tile__description > div > span')
        WebDriverWait(driver, timeout).until(element_present)
        content = driver.page_source
        from lxml import html
        tree = html.fromstring(content)
        driver.close()
        return tree
    except Exception as err:
        print(err)
        try:
            driver.close()
        except:
            pass


def checkStores(update, context):
    urls = []

    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='Где же ты плоечка, где же ты где...')

    company_name = '1C Интерес'
    xpath_status = '//*[@id="base"]/div[2]/div[2]/div[2]/div[2]/p/a'
    xpath_btn = '//*[@id="base"]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/span/a/span'
    digitalUrl = 'https://www.1c-interes.ru/catalog/all6969/30328284/'
    diskUrl = 'https://www.1c-interes.ru/catalog/all6969/30328282/'
    tree, rawHTML = getPage(digitalUrl)
    status = getInfoByXpath(xpath_status, tree)
    btn = getInfoByXpath(xpath_btn, tree)
    type = 'Digital'
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + digitalUrl + '">'
                                  + company_name
                                  + ', ' + type + ',\n' + status
                                  + '\n' + btn
                                  + '</a>',
                             disable_web_page_preview='True')

    tree, rawHTML = getPage(diskUrl)
    status = getInfoByXpath(xpath_status, tree)
    btn = getInfoByXpath(xpath_btn, tree)
    type = 'Disk'
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + diskUrl + '">'
                                  + company_name
                                  + ', ' + type + ',\n' + status
                                  + '\n' + btn
                                  + '</a>',
                             disable_web_page_preview='True')

    company_name = 'М.видео'
    # mvideo_xpath_status_digital = '//*[class="c-notifications__title"]'
    mvideo_xpath_status_disk = '//*[@id="js-product-tile-list"]/div/div[1]/div[3]/div/span'
    mvideo_xpath_status_digital2 = '/html/body/div[3]/div[1]/div[3]/div/div[3]/div[2]/div/div[3]/div[1]/div[3]/a'

    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='plz, wait', disable_web_page_preview='True')

    # mvideo_disk_digital_url = 'https://www.mvideo.ru/promo/sony-ps5'
    mvideo_digital_url = 'https://www.mvideo.ru/products/igrovaya-konsol-sony-playstation-5-digital-edition-40074203'
    mvideo_disk_url = 'https://www.mvideo.ru/products/igrovaya-konsol-sony-playstation-5-40073270'
    # tree, rawHTML = getPage(mvideo_disk_digital_url)
    # status = getInfoByXpath(mvideo_xpath_status_digital, tree)
    xpath_status = r'//*[@id="showcase"]/div/div[3]/div[2]/div/div[1]/div[3]'
    sel1 = r'body > div.wrapper > div.page-content > div.main-holder > div > div.product-main-information.section > div.o-container__price-column > div > div.fl-pdp-pay.o-pay.u-mb-8 > div.o-pay__content > div.c-notifications.u-mt-16 > div > div > span'

    # tree2 = getTreeByXpath2(mvideo_disk_digital_url, mvideo_xpath_status_digital)
    try:
        rawHtml, tree = getTreeByXpath(mvideo_digital_url, xpath_status)
        status = tree.xpath(xpath_status)[0].text.strip()
    except:
        status = ''

    type = 'Digital'
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + mvideo_digital_url + '">'
                                  + company_name
                                  + ', ' + type + ',\n' + status
                                  #+ '\n' + status2
                                  + '</a>',
                             disable_web_page_preview='True')

    # status = getInfoByXpath(mvideo_xpath_status_disk, tree)
    type = 'Disk'
    try:
        # rawHtml, tree = getTreeByXpath(mvideo_disk_url, xpath_status)
        status = tree.xpath(mvideo_xpath_status_digital)[0].text.strip()
        status2 = tree.xpath(mvideo_xpath_status_digital2)[0].text.strip()
    except:
        status = ''
        status2 = ''

    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + mvideo_disk_url + '">'
                                  + company_name
                                  + ', ' + type + ',\n' + status + '\n' + status2
                                  + '</a>',
                             disable_web_page_preview='True')

    company_name = 'Sony.ru'
    sony_xpath_status = '/html/body/div[3]/div[3]/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]'
    url_sony_digital = 'https://store.sony.ru/product/konsol-playstation-5-digital-edition-317400/'
    url_sony_disk = 'https://store.sony.ru/product/konsol-playstation-5-317406/'

    tree, rawHTML = getPage(url_sony_digital)
    selector_btn = r'body > div.body > div.rel.with-image.with-image > div.product-top.top-header.fixy.js-prod-detail.\33 17400 > div.container.product-top__cont > div.pricebox.pricebox-card.clearfix > div.item-button.sold_out_button > span'
    sel2 = r'body > div.body > div.rel.with-image.with-image > div.product-top.top-header.fixy.js-prod-detail.\33 17400 > div.container.product-top__cont > div.pricebox.pricebox-card.clearfix > div.item-price-wrapper > div.item-availability.hidden-mv > div.availability.a-preorder'
    status1 = get_text_by_selector(rawHTML, sel2)
    status2 = get_text_by_selector(rawHTML, selector_btn)
    type = 'Digital'
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + url_sony_digital + '">'
                                  + company_name
                                  + ', ' + type + ', \n' + status1 + ',\n' + status2
                                  + '</a>',
                             disable_web_page_preview='True')

    tree, rawHTML = getPage(url_sony_disk)
    selector_btn = r'body > div.body > div.rel.with-image.with-image > div.product-top.top-header.fixy.js-prod-detail.\33 17406 > div.container.product-top__cont > div.pricebox.pricebox-card.clearfix > div.item-button.sold_out_button > span'
    sel2 = r'body > div.body > div.rel.with-image.with-image > div.product-top.top-header.fixy.js-prod-detail.\33 17406 > div.container.product-top__cont > div.pricebox.pricebox-card.clearfix > div.item-price-wrapper > div.item-availability.hidden-mv > div.availability.a-preorder'
    status1 = get_text_by_selector(rawHTML, sel2)
    status2 = get_text_by_selector(rawHTML, selector_btn)
    type = 'Disk'
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + url_sony_disk + '">'
                                  + company_name
                                  + ', ' + type + ', \n' + status1 + ',\n' + status2
                                  + '</a>',
                             disable_web_page_preview='True')

    # Эльдорадо
    company_name = 'Эльдорадо'
    xpath_status = '//*[@id="showcase"]/div/div[3]/div[2]/div/div[1]/div[3]'
    xpath_status2 = '//*[@id="showcase"]/div/div[3]/div[2]/div/div[1]/div[4]/a'
    url_eldorado_disk = 'https://www.eldorado.ru/cat/detail/igrovaya-pristavka-sony-playstation-5/'
    url_eldorado_digital = 'https://www.eldorado.ru/cat/detail/igrovaya-pristavka-playstation-5-digital-edition/'

    # tree, rawHTML = getPage(url_eldorado_digital)
    # status = getInfoByXpath(xpath_status, tree)
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='plz, wait', disable_web_page_preview='True')
    try:
        rawHtml, tree = getTreeByXpath(url_eldorado_digital, xpath_status)
        status = tree.xpath(xpath_status)[0].text.strip()
        status2 = tree.xpath(xpath_status2)[0].text.strip()
    except:
        pass

    # status2 = getInfoByXpath(xpath_status2, tree)
    # tree2 = getPageByXpath(url_sony_digital, eldorado_btn)
    # btn_info = tree2.xpath(eldorado_btn)[0].text.strip()
    type = 'Digital'
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + url_eldorado_digital + '">'
                                  + company_name + ', ' + type + ',\n' + status + ',\n' + status2
                                  # + '\n' + btn_info
                                  + '</a>', disable_web_page_preview='True')

    # tree, rawHTML = getPage(url_eldorado_disk)
    # status = getInfoByXpath(xpath_status, tree)
    # status2 = getInfoByXpath(xpath_status2, tree)
    try:
        rawHtml, tree = getTreeByXpath(url_eldorado_disk, xpath_status)
        status = tree.xpath(xpath_status)[0].text.strip()
        status2 = tree.xpath(xpath_status2)[0].text.strip()
    except:
        pass
    type = 'Disk'
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + url_eldorado_disk + '">'
                                  + company_name + ', ' + type + ',\n' + status + ',\n' + status2
                                  + '</a>', disable_web_page_preview='True')

    # Ozon
    company_name = 'Ozon'
    xpath_status = '//*[@id="__ozon"]/div/div[1]/div[4]/div[3]/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div/div[1]'
    xpath_status_btn = '//*[@id="__ozon"]/div/div[1]/div[4]/div[3]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/button/div/div'
    url_ozon_disk = 'https://www.ozon.ru/product/igrovaya-konsol-playstation-5-belyy-178337786/'
    url_ozon_digital = 'https://www.ozon.ru/product/igrovaya-pristavka-playstation-5-digital-edition-belyy-178715781/'
    tree, rawHTML = getPage(url_ozon_digital)
    status = getInfoByXpath(xpath_status, tree)
    status_btn = getInfoByXpath(xpath_status_btn, tree)
    type = 'Digital'
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + url_ozon_digital + '">'
                                  + company_name + ', ' + type + ',\n' + status + ',\n' + status_btn
                                  + '</a>',
                             disable_web_page_preview='True')

    tree, rawHTML = getPage(url_ozon_disk)
    status = getInfoByXpath(xpath_status, tree)
    status_btn = getInfoByXpath(xpath_status_btn, tree)
    type = 'Disk'
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + url_ozon_disk + '">'
                                  + company_name + ', ' + type + ',\n' + status + ',\n' + status_btn
                                  + '</a>',
                             disable_web_page_preview='True')

    # DNS
    company_name = 'DNS-shop'
    xpath_status = r'//*[@id="product-page"]/div[3]/div[2]/div[1]/div[3]/div[4]/div[2]/div[1]/button'
    xpath_status2 = r'//*[@id="product-page"]/div[3]/div[2]/div[1]/div[3]/div[3]/div[2]/div[3]/div/span'
    url_dns_digital = 'https://www.dns-shop.ru/product/44f657d4ac493332/igrovaa-konsol-playstation-5-digital-edition/'
    type = 'Digital'
    # context.bot.send_message(chat_id=update.message.chat_id,
    #                          parse_mode=ParseMode.HTML,
    #                          text='Долгая обработка ' + company_name + ', пжлст, ждите')
    try:
        tree = ''
        # tree = getTreeByXpath(url_dns_digital, xpath_status)
        # status = tree.xpath(xpath_status)[0].text.strip()
        # status2 = tree.xpath(xpath_status2)[0].text.strip()
        # context.bot.send_message(chat_id=update.message.chat_id,
        #                          parse_mode=ParseMode.HTML,
        #                          text='<a href="' + url_dns_digital + '">'
        #                                 + company_name + ', ' + type + ',\n' + status2 + ',\n' + status
        #                               + '</a>', disable_web_page_preview='True')
    except Exception as err:
        logger.info(err)

    # GamePark
    company_name = 'GamePark'
    xpath_status = '//*[@id="content"]/div/div/div[3]/div[1]/div[2]/div/a'
    url_gamepark_digital = 'https://www.gamepark.ru/playstation5/console/IgrovayakonsolSonyPlayStation5DigitalEdition/'
    url_gamepark_disk = 'https://www.gamepark.ru/playstation5/console/IgrovayakonsolSonyPlayStation5/'
    tree, rawHTML = getPage(url_gamepark_digital)
    type = 'Digital'
    status = getInfoByXpath(xpath_status, tree)
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + url_gamepark_digital + '">'
                                  + company_name
                                  + ', ' + type + ',\n' + status
                                  + '</a>',
                             disable_web_page_preview='True')

    tree, rawHTML = getPage(url_gamepark_disk)
    status = getInfoByXpath(xpath_status, tree)
    type = 'Disk'
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + url_gamepark_disk + '">'
                                  + company_name
                                  + ', ' + type + ',\n' + status
                                  + '</a>',
                             disable_web_page_preview='True')

    # Видеоигр.net
    company_name = 'ВидеоИгорь'
    xpath_status = '//*[@id="cart_quantity"]/div/div/div[3]/span[2]'
    url_videoigr_digital = 'https://videoigr.net/product_info/igrovaya-pristavka-playstation-5-digital-edition/21202/'
    url_videoigr_disk = 'https://videoigr.net/product_info/igrovaya-pristavka-playstation-5/21201/'
    tree, rawHTML = getPage(url_videoigr_digital)
    status = getInfoByXpath(xpath_status, tree)
    type = 'Digital'
    xpath2 = '//*[@id="cart_quantity"]/div/div/div[9]/div/div'
    status2 = getInfoByXpath(xpath2, tree)
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + url_videoigr_digital + '">'
                                  + company_name
                                  + ', ' + type + ',\n' + status + '\n' + status2
                                  + '</a>',
                             disable_web_page_preview='True')

    tree, rawHTML = getPage(url_videoigr_disk)
    status = getInfoByXpath(xpath_status, tree)
    type = 'Disk'
    status2 = getInfoByXpath(xpath2, tree)
    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text='<a href="' + url_videoigr_disk + '">'
                                  + company_name
                                  + ', ' + type + ',\n' + status + '\n' + status2
                                  + '</a>',
                             disable_web_page_preview='True')

    context.bot.send_message(chat_id=update.message.chat_id,
                             parse_mode=ParseMode.HTML,
                             text="Все магазы проверены,\nМарки тоже наклеены...\nThis is the end, my only friend, the end.")

    try:
        deemojitext = ''
        deemojitext = demoji.replace(update.message.text, "")
        logger.info('Запрос от: '
                    + str(update.message.from_user.full_name)
                    + ',  ' + str(update.message.date)
                    + ', ' + deemojitext)
    except Exception as err:
        logger.info('Запрос мутный, эмодзи или коды: '
                    + str(update.message.from_user.full_name)
                    + ',  ' + str(update.message.date))


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    try:
        deemojitext = ''
        deemojitext = demoji.replace(update.message.text, "")
        logger.info('Запрос от: '
                    + str(update.message.from_user.full_name)
                    + ',  ' + str(update.message.date)
                    + ', ' + deemojitext)
    except Exception as err:
        logger.info('Запрос мутный, эмодзи или коды: '
                    + str(update.message.from_user.full_name)
                    + ',  ' + str(update.message.date))

    try:
        # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        #     executor.map(checkStores, (update, context))
        # threading.Thread(target=checkStores, args=(update, context), daemon=True).start()
        context.bot.send_message(chat_id=update.message.chat_id,
                                 parse_mode=ParseMode.HTML,
                                 text='Zed is dead, baby, Zed is dead….')
        #
        # print(rawHTML)
    except Exception as err:
        print(err)

def getPage(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.66 Safari/537.36 OPR/72.0.3815.378'}

        r = requests.get(url, headers=headers, timeout=20)
        content = r.text
        from lxml import html
        tree = html.fromstring(content)
    except:
        tree = ''
        content = ''
    return tree, content

def getInfoByXpath(xpathurl, tree):
    try:
        status = (tree.xpath(xpathurl)[0].text).strip()
    except:
        status = 'Ошибка'

    return status


def main():
    demoji.download_codes()

    token = '2463413634_:_AAHrTvhbCSUE1e74TDR9QmOD702rk_PjNhc'
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # Начинаем поиск обновлений
    updater.start_polling()
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger = Logger('Main', r'E:\ya.disk\gdeps5\gdeps5\log.log')
    logger.info('Start ROBOT')
    main()
