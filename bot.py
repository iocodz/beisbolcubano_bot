from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from env import API_KEY
from bs4 import BeautifulSoup as bso

import requests
from functools import wraps


def getSoup():
    url = 'http://www.beisbolcubano.cu/'
    html = requests.get(url)
    soup = bso(html.text, 'lxml')

    return soup


def getResults():
    soup = getSoup()
    runs = soup.find_all('span', {"class": "Mini_DayScore_Runs"})
    siglas = soup.find_all('span', {"class": "Mini_DayScore_Siglas"})

    results = ''

    for i in range(0 , len(runs) // 2, 2):
        results += ('%s %s - %s %s\n' % (siglas[i].text, runs[i].text, siglas[i + 1].text, runs[i + 1].text))

    return results


def getTabla():
    soup = getSoup()
    data = soup.find_all('h5', {"class": "h5_margin_top"})
    teams = soup.find_all('span', {"style": "position:absolute; margin:13px 0 0 5px;"})

    tabla = ''
    amount_teams = len(teams)
    for i in range(amount_teams):
        tabla += ('%s. %s - %s - %s - %s\n' % (i + 1, teams[i].text, data[(i + 1) * amount_teams].text, data[(i + 1) * amount_teams + 1].text, data[(i + 1) * amount_teams + 2].text))

    return tabla


def tabla(bot, update):
    chat_id = update.message.chat_id

    tabla = getTabla()
    bot.send_message(chat_id=chat_id, text=tabla)


def resultados(bot, update):
    chat_id = update.message.chat_id
    
    results = getResults()

    bot.send_message(chat_id=chat_id, text=results)
    bot.send_message(chat_id=chat_id, text='Si no aparecen los resultados completos pude que no se hallan celebrado los partidos aún.')


def main():
    updater = Updater(API_KEY)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('tabla', tabla))
    dp.add_handler(CommandHandler('resultados', resultados))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

