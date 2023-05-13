# -*- coding: utf-8 -*-

import os, sys, re, json
import urllib.request
import urllib.parse
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import CommonFunctions

PLUGIN_NAME   = 'CurrentTime.TV'

common = CommonFunctions
common.plugin = PLUGIN_NAME


BASE_URL = "https://www.currenttime.tv"

stream_url = {
    'Auto (hls)': 'https://rfe-ingest.akamaized.net/hls/live/2033043/tvmc05/master.m3u8',
    'Auto (mpd)': 'https://rfe-ingest.akamaized.net/dash/live/2033030/tvmc05/manifest.mpd',
    'rtmp': 'rtmp://cp107825.live.edgefcs.net/live/rfe_tvmc5@383651',
}

try:handle = int(sys.argv[1])
except:pass

def xt(x): return xbmcvfs.translatePath(x)

addon = xbmcaddon.Addon(id='plugin.video.evld.currenttime.tv')

Pdir = addon.getAddonInfo('path')
icon = xt(os.path.join(Pdir, 'icon.png'))
fanart = xt(os.path.join(Pdir, 'fanart.jpg'))

fanarts = {
    'vecher/episodes':xt(os.path.join(Pdir, 'media', 'vecher.jpg')),
    'glavnoe/episodes':xt(os.path.join(Pdir, 'media', 'glavnoe.jpg')),
    'doc/episodes':xt(os.path.join(Pdir, 'media', 'doc.jpg')),
    'unknownrussia/episodes':xt(os.path.join(Pdir, 'media', 'unknownrussia.jpg')),
    'unknownbelarus/episodes':xt(os.path.join(Pdir, 'media', 'unknownbelarus.jpg')),
    'person/episodes':xt(os.path.join(Pdir, 'media', 'person.jpg')),
    'series/episodes':xt(os.path.join(Pdir, 'media', 'series.jpg')),
    'smotrivoba/episodes':xt(os.path.join(Pdir, 'media', 'smotrivoba.jpg')),
    'welcome/episodes':xt(os.path.join(Pdir, 'media', 'welcome.jpg')),
    'asia/episodes':xt(os.path.join(Pdir, 'media', 'asia.jpg')),
    'baltia/episodes':xt(os.path.join(Pdir, 'media', 'baltia.jpg')),
    'amerika/episodes':xt(os.path.join(Pdir, 'media', 'amerika.jpg')),
    'priznaki/episodes':xt(os.path.join(Pdir, 'media', 'priznaki.jpg')),
    'utro/episodes':xt(os.path.join(Pdir, 'media', 'utro.jpg')),
    'asia-360/episodes':xt(os.path.join(Pdir, 'media', 'asia-360.jpg')),
    'z/21370/episodes':xt(os.path.join(Pdir, 'media', 'roadtrip.jpg')),
    'z/20708/episodes':xt(os.path.join(Pdir, 'media', 'news.jpg')),
    'https://www.svoboda.org/z/959':xt(os.path.join(Pdir, 'media', 'svoboda.jpg')),
    'https://www.svoboda.org/music/episodes':xt(os.path.join(Pdir, 'media', 'svoboda.jpg')),
    'https://www.golosameriki.com/z/5943':xt(os.path.join(Pdir, 'media', 'voa.jpg')),
    'https://www.golosameriki.com/z/5944':xt(os.path.join(Pdir, 'media', 'voa.jpg')),
    'https://www.svoboda.org/z/16307/episodes':xt(os.path.join(Pdir, 'media', 'svoboda.jpg')),
    'https://www.svoboda.org/z/22459/episodes':xt(os.path.join(Pdir, 'media', 'svoboda.jpg')),
}

icons = {
    'z/21701':xt(os.path.join(Pdir, 'media', 'listen.jpg')),
    'z/21950':xt(os.path.join(Pdir, 'media', 'kgb.jpg')),
    'svoboda':xt(os.path.join(Pdir, 'media', 'svoboda.png')),
    'z/5943':xt(os.path.join(Pdir, 'media', 'president.jpg')),
    'z/5944':xt(os.path.join(Pdir, 'media', 'talk.jpg')),
    'music/episodes':xt(os.path.join(Pdir, 'media', 'music.jpg')),
    'z/16307':xt(os.path.join(Pdir, 'media', 'pravo.jpg')),
    'z/22459':xt(os.path.join(Pdir, 'media', '911.jpg')),
}

xbmcplugin.setContent(handle, 'videos')

def get_html(url, params={}, noerror=True):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    if params:
        url = '%s?%s' % (url, urllib.parse.urlencode(params))

    conn = urllib.request.urlopen(urllib.request.Request(url, headers=headers))
    html = conn.read()
    conn.close()

    if conn.headers.get_content_charset():
        html = html.decode(conn.headers.get_content_charset())

    return html 


def main_menu():
    add_item('[B]Смотреть ТВ[/B]', {'mode':'live'}, icon=icon, fanart=fanart, isPlayable=True)
    
    if addon.getSetting('LastNews') == 'true':
        show_content({'mode':'program', 'u':'p/7363.html'}) # Новости. Коротко (последний выпуск)
    else:
        add_item('Новости', {'mode':'program', 'u':'z/20708/episodes'}, fanart=fanart, isFolder=True)

    add_item('Избранные программы', {'mode':'programs'}, fanart=fanart, isFolder=True)
    add_item('Эфиры', {'mode':'program', 'u':'z/17317'}, fanart=fanart, isFolder=True)
    add_item('Репортажи', {'mode':'program', 'u':'report/episodes'}, fanart=fanart, isFolder=True)
    add_item('Интервью', {'mode':'program', 'u':'interview/episodes'}, fanart=fanart, isFolder=True)
    add_item('Всё видео', {'mode':'program', 'u':'z/17192'}, fanart=fanart, isFolder=True)
    add_item('Подкасты', {'mode':'podcasts'}, fanart=fanart, isFolder=True)
    if addon.getSetting('ShowRF') == 'true':
        add_item('Радио Свобода', {'mode':'program', 'u':'https://www.svoboda.org/z/959', 'b':'https://www.svoboda.org'}, fanart=fanarts['https://www.svoboda.org/z/959'], isFolder=True)
    add_item('Поиск', {'mode':'search'}, fanart=fanart, icon='DefaultAddonsSearch.png', isFolder=True)
    xbmcplugin.endOfDirectory(handle)


def programs():
    add_item('Главное', {'mode':'program', 'u':'glavnoe/episodes'}, icon=icon, fanart=fanarts['glavnoe/episodes'], isFolder=True)
    add_item('Утро', {'mode':'program', 'u':'utro/episodes'}, icon=icon, fanart=fanarts['utro/episodes'], isFolder=True)
    add_item('Вечер', {'mode':'program', 'u':'vecher/episodes'}, icon=icon, fanart=fanarts['vecher/episodes'], isFolder=True)
    add_item('Реальное кино', {'mode':'program', 'u':'doc/episodes'}, icon=icon, fanart=fanarts['doc/episodes'], isFolder=True)
    add_item('Настоящий сериал', {'mode':'program', 'u':'series/episodes'}, icon=icon, fanart=fanarts['series/episodes'], isFolder=True)
    add_item('Неизвестная Россия', {'mode':'program', 'u':'unknownrussia/episodes'}, icon=icon, fanart=fanarts['unknownrussia/episodes'], isFolder=True)
    add_item('Признаки жизни', {'mode':'program', 'u':'priznaki/episodes'}, icon=icon, fanart=fanarts['priznaki/episodes'], isFolder=True)
    add_item('Человек на карте', {'mode':'program', 'u':'person/episodes'}, icon=icon, fanart=fanarts['person/episodes'], isFolder=True)
    add_item('Смотри в оба', {'mode':'program', 'u':'smotrivoba/episodes'}, icon=icon, fanart=fanarts['smotrivoba/episodes'], isFolder=True)
    add_item('Ждём в гости', {'mode':'program', 'u':'welcome/episodes'}, icon=icon, fanart=fanarts['welcome/episodes'], isFolder=True)
    add_item('Балтия', {'mode':'program', 'u':'baltia/episodes'}, icon=icon, fanart=fanarts['baltia/episodes'], isFolder=True)
    add_item('Азия', {'mode':'program', 'u':'asia/episodes'}, icon=icon, fanart=fanarts['asia/episodes'], isFolder=True)
    add_item('Азия 360°', {'mode':'program', 'u':'asia-360/episodes'}, icon=icon, fanart=fanarts['asia-360/episodes'], isFolder=True)
    add_item('Америка', {'mode':'program', 'u':'amerika/episodes'}, icon=icon, fanart=fanarts['amerika/episodes'], isFolder=True)
    add_item('Америка. Большое путешествие', {'mode':'program', 'u':'z/21370/episodes'}, icon=icon, fanart=fanarts['z/21370/episodes'], isFolder=True)
    add_item('Неизвестная Беларусь', {'mode':'program', 'u':'unknownbelarus/episodes'}, icon=icon, fanart=fanarts['unknownbelarus/episodes'], isFolder=True)
    xbmcplugin.endOfDirectory(handle)


def podcasts():
    add_item('Послушайте! Олевский', {'mode':'program', 'u':'z/21701'}, icon=icons['z/21701'], fanart=fanart, plot='Слушайте подкасты Тимура Олевского. Журналист телеканала "Настоящее Время" ищет ответы на свои вопросы. "Я задумал этот подкаст для того, чтобы изучить и рассказать о том, что не идет у меня из головы", – говорит Олевский', isFolder=True)
    add_item('Архивы КГБ', {'mode':'program', 'u':'z/21950'}, icon=icons['z/21950'], fanart=fanart, plot='Подкаст "Архивы КГБ" — это истории, найденные киевским журналистом и историком Эдуардом Андрющенко в рассекреченных документах КГБ Украины.', isFolder=True)
    if addon.getSetting('ShowVOA') == 'true':
        add_item('Президентские истории', {'mode':'program', 'u':'https://www.golosameriki.com/z/5943', 'b':'https://www.golosameriki.com'}, icon=icons['z/5943'], fanart=fanarts['https://www.golosameriki.com/z/5943'], plot='Истории о людях, управлявших и управляющих Соединенными Штатами Америки', isFolder=True)
        add_item('Знаем Talk', {'mode':'program', 'u':'https://www.golosameriki.com/z/5944', 'b':'https://www.golosameriki.com'}, icon=icons['z/5944'], fanart=fanarts['https://www.golosameriki.com/z/5944'], plot='Знаем Talk – это еженедельный подкаст о языке, на котором мы говорим, и о языках, которые нас окружают', isFolder=True)
    if addon.getSetting('ShowRF') == 'true':
        add_item('Музыка на "Свободе"', {'mode':'program', 'u':'https://www.svoboda.org/music/episodes', 'b':'https://www.svoboda.org'}, icon=icons['music/episodes'], fanart=fanarts['https://www.svoboda.org/music/episodes'], plot='Артемий Троицкий, музыкальный критик и активист широкого профиля, представляет в своём подкасте и его радиоверсии талантливую новую музыку самых разных стилей и направлений.', isFolder=True)
        add_item('Человек имеет право', {'mode':'program', 'u':'https://www.svoboda.org/z/16307/episodes', 'b':'https://www.svoboda.org'}, icon=icons['z/16307'], fanart=fanarts['https://www.svoboda.org/z/16307/episodes'], plot='Всё, что происходит в жизни каждого, связано с правами и свободами. Право на выбор, право на жизнь и здоровье, право на самовыражение и многое другое. “Человек имеет право” — это подкаст, который ведем мы, судебные обозреватели Радио Свобода Марьяна Торочешникова и Наталья Джанполадова. Вместе мы выясняем, как устроен окружающий нас мир прав и обязанностей, почему он устроен именно так и что делать, чтобы отстоять свои права.', isFolder=True)
        add_item('После 9/11', {'mode':'program', 'u':'https://www.svoboda.org/z/22459/episodes', 'b':'https://www.svoboda.org'}, icon=icons['z/22459'], fanart=fanarts['https://www.svoboda.org/z/16307/episodes'], plot='Теракт 11 сентября 2001 года — огромная катастрофа XXI века. Тот день изменил миллионы людей: тех кто тогда были в Нью-Йорке и тех, кто были за тысячи километров. Спустя 20 лет мы поговорили с людьми об их жизни после 9/11 и попытались понять, как историческое событие влияет на обычных людей.', isFolder=True)
    xbmcplugin.endOfDirectory(handle)


def play(url, title=None):
    item = xbmcgui.ListItem(path=url)

    if title:
        item.setInfo(type='video', infoLabels={'title':title})

    if '.mpd' in url:
        item.setProperty('inputstream', 'inputstream.adaptive')
        item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
        item.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
        item.setProperty('inputstream.adaptive.license_key', 'https://cwip-shaka-proxy.appspot.com/no_auth||R{SSM}|')
    elif '.m3u' in url:
        item.setProperty('inputstream', 'inputstream.adaptive')
        item.setProperty('inputstream.adaptive.manifest_type', 'hls')

    xbmcplugin.setResolvedUrl(handle, True, item)


def live():
    quality = addon.getSetting('LiveQuality')

    purl = stream_url.get(quality, stream_url['Auto (hls)'])

    if '.m3u' in purl:
        if quality[:4] != 'Auto':
            m3u8 = get_html(purl)
            streams = re.findall(r'x(\d+).*?(http.*?)$', m3u8, flags=re.MULTILINE | re.DOTALL)
            stream = [s[1] for s in streams if '{}p'.format(s[0]) == quality]
            if stream:
                purl = stream[0]

    play(purl, 'Live')


def show_content(params):
    page = int(params.get('p', 0))

    url = params['u'] = urllib.parse.unquote_plus(params['u']).lstrip('/')
    base = urllib.parse.unquote_plus(params.get('b', BASE_URL))

    html = get_html(url if url[:4] == 'http' else '%s/%s' % (base, url), {'p':page})

    container = common.parseDOM(html, 'div', attrs={'class':'media-block-wrap'})

    if url != 'p/7363.html':
        container = container[0]

    is_news = url == 'z/20708/episodes'

    blocks = common.parseDOM(container, 'div', attrs={'class':'media-block .*?'})

    for block in blocks:

        href = common.parseDOM(block, 'a', attrs={'class':'img-wrap.*?'}, ret='href')
        if not href:
            continue

        href = href[0]

        title = common.parseDOM(block, 'a', attrs={'class':'img-wrap.*?'}, ret='title')[0]
        title = common.replaceHTMLCodes(title)
        img = common.parseDOM(block, 'img', ret='src')[0]
        date = common.parseDOM(block, 'span', attrs={'class':'date .*?'})

        if is_news:
            plot = title.capitalize()
            title = date[0] if date else title
        else:
            plot = '[B]{0}[/B]\n\n{1}'.format(date[0] if date else '', title)

        thumb = re.sub(r'_w\w+', '_w512_r1', img)

        fan = fanarts.get(url, fanart)
        if addon.getSetting('DownloadFanart') == 'true':
            fan = re.sub(r'_w\w+', '_w1920_r1', img)

        item_params = params.copy()
        item_params.update({'mode':'play', 'u':href})
        add_item(title, item_params, thumb=thumb, plot=plot, fanart=fan, isPlayable=True)


    if common.parseDOM(html, 'p', attrs={'class':'buttons btn--load-more'}) and not is_news:
        params['p'] = page + 1
        fan = fanarts.get(url, fanart)
        add_item('Далее > %i' % (1 + params['p']), params, fanart=fan, isFolder=True)


def program(params):
    show_content(params)
    xbmcplugin.endOfDirectory(handle)


def play_video(params):
    url = urllib.parse.unquote_plus(params['u']).lstrip('/')
    base = urllib.parse.unquote_plus(params.get('b', BASE_URL))

    html = get_html(url if url[:4] == 'http' else '%s/%s' % (base, urllib.parse.quote(url)))

    quality = addon.getSetting('VideoQuality')

    frame = re.compile(r'<meta content="(.+?)" name="twitter:player"').findall(html)

    html = get_html(frame[0])

    data = re.compile(r'data-sources="(.+?)" data-lt-on-play="').findall(html)
    if data:
        data = json.loads(common.replaceHTMLCodes(data[0]))

        for video in data:
            if quality == video['DataInfo'].replace('270', '240'):
                purl = video['AmpSrc']
                break
        else:
            purl = data[-1]['AmpSrc']
    else:
        audio = common.parseDOM(html, 'audio', ret='src')
        if audio:
            purl = audio[0]

    play(purl)


def search(params):
    page = int(params.get('p', 1))

    keywords = urllib.parse.unquote_plus(params.get('k', ''))

    if not keywords:
        kbd = xbmc.Keyboard('', 'Поиск:')
        kbd.doModal()
        xbmcplugin.endOfDirectory(handle, cacheToDisc=False)
        if kbd.isConfirmed():
            keywords = kbd.getText()
            if keywords:
                xbmc.executebuiltin('Container.Update(%s?mode=search&k=%s, replace)' % (sys.argv[0], urllib.parse.quote_plus(keywords)))
                return
        xbmc.executebuiltin('Container.Update(%s, replace)' % sys.argv[0])

    else:
        html = get_html('%s/s' % BASE_URL, {'k':keywords, 'tab':'video', 'pi':page, 'r':'any', 'pp':20})

        videos = common.parseDOM(html, 'div', attrs={'class':'media-block '})

        for video in videos:
            img = common.parseDOM(video, 'img', ret='src')[0]
            href = common.parseDOM(video, 'a', attrs={'class':'img-wrap.*?'}, ret="href")[0]
            title = common.parseDOM(video, 'a', attrs={'class':'img-wrap.*?'}, ret="title")[0]
            date = common.parseDOM(video, 'span', attrs={'class':'date .*?'})[0]

            thumb = re.sub(r'_w\w+', '_w512_r1', img)

            title = common.replaceHTMLCodes(title)

            info = common.parseDOM(video, 'p', attrs={'class':'perex .*?'})
            plot = '[B]%s[/B]\n%s' % (date, common.replaceHTMLCodes(info[0]) if info else '')

            add_item(title, {'mode':'play', 'u':href}, plot=plot, thumb=thumb, fanart=fanart, isPlayable=True)

        if common.parseDOM(html, 'span', attrs={'class':'ico ico-arrow-forward'}):
            params.update({'p':page + 1, 'k':keywords})
            add_item('Далее > %i' % (params['p']), params, fanart=fanart, isFolder=True)


        xbmcplugin.setPluginCategory(handle, 'Search')
        xbmcplugin.endOfDirectory(handle)


def add_item(title, params={}, icon='', banner='', fanart='', poster='', thumb='', plot='', isFolder=False, isPlayable=False, url=None):
    item = xbmcgui.ListItem(title)
    item.setInfo(type='Video', infoLabels={'title': title, 'plot': plot})

    if isPlayable:
        item.setProperty('mediatype', 'video')
        item.setProperty('isPlayable', 'true')
    
    if icon != '':
        item.setArt({'icon': icon})
    if thumb != '':
        item.setArt({'thumb': thumb})
    if banner != '':
        item.setArt({'banner': banner})
    if fanart != '':
        item.setArt({'fanart': fanart})
    if poster != '':
        item.setArt({'poster': poster})
    if thumb != '':
        item.setArt({'thumb': thumb})

    if url is None:
        url = '%s?%s' % (sys.argv[0], urllib.parse.urlencode(params))
        item.setContentLookup(False)

    xbmcplugin.addDirectoryItem(handle, url=url, listitem=item, isFolder=isFolder)


params = common.getParameters(sys.argv[2])

mode = params.get('mode', '')

if mode == '':
    main_menu()

elif mode == 'live':
    live()

elif mode == 'programs':
    programs()

elif mode == 'podcasts':
    podcasts()

elif mode == 'program':
    program(params)

elif mode == 'play':
    play_video(params)

elif mode == 'search':
    search(params)

elif mode == 'cleancache':
    from tccleaner import TextureCacheCleaner as tcc
    tcc().remove_like('%currenttime.tv%', True)
    tcc().remove_like('%rferl.org%', True)
    tcc().remove_like('%voanews.com%', True)
