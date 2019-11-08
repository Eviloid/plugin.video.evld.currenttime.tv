#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, urllib, sys, urllib2, re, json
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import CommonFunctions

PLUGIN_NAME   = 'CurrentTime.TV'

common = CommonFunctions
common.plugin = PLUGIN_NAME


BASE_URL = "https://www.currenttime.tv"

stream_url = {
    'Auto (hls)': 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/master.m3u8',
    'Auto (mpd)': 'https://rfeingest-i.akamaihd.net/dash/live/677329-b/DASH_RFE-TVMC5/manifest.mpd',
    '1080p':'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/index_1080_av-p.m3u8',
    '720p': 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/index_0720_av-p.m3u8',
    '540p': 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/index_0540_av-p.m3u8',
    '404p': 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/index_0404_av-p.m3u8',
    '288p': 'http://rfe-lh.akamaihd.net/i/rfe_tvmc5@383630/index_0288_av-p.m3u8',
    'rtmp': 'rtmp://cp107825.live.edgefcs.net/live/rfe_tvmc5@383651'
}

try:handle = int(sys.argv[1])
except:pass

addon = xbmcaddon.Addon(id='plugin.video.evld.currenttime.tv')

Pdir = addon.getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(Pdir, 'icon.png'))
fanart = xbmc.translatePath(os.path.join(Pdir, 'fanart.jpg'))

fanarts = {
    'vecher/episodes':xbmc.translatePath(os.path.join(Pdir, 'media', 'vecher.jpg')),
    'glavnoe/episodes':xbmc.translatePath(os.path.join(Pdir, 'media', 'glavnoe.jpg')),
    'doc/episodes':xbmc.translatePath(os.path.join(Pdir, 'media', 'doc.jpg')),
    'unknownrussia/episodes':xbmc.translatePath(os.path.join(Pdir, 'media', 'unknownrussia.jpg')),
    'person/episodes':xbmc.translatePath(os.path.join(Pdir, 'media', 'person.jpg')),
    'series/episodes':xbmc.translatePath(os.path.join(Pdir, 'media', 'series.jpg')),
    'smotrivoba/episodes':xbmc.translatePath(os.path.join(Pdir, 'media', 'smotrivoba.jpg')),
    'asia/episodes':xbmc.translatePath(os.path.join(Pdir, 'media', 'asia.jpg')),
    'amerika/episodes':xbmc.translatePath(os.path.join(Pdir, 'media', 'amerika.jpg'))
}

xbmcplugin.setContent(handle, 'videos')

def get_html(url, params={}, noerror=True):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    conn = urllib2.urlopen(urllib2.Request('%s?%s' % (url, urllib.urlencode(params)), headers=headers))
    html = conn.read()
    conn.close()

    return html 


def main_menu():
    add_item('[B]Смотреть ТВ[/B]', {'mode':'live'}, icon=icon, fanart=fanart, isPlayable=True)
    show_content({'mode':'program', 'u':'p/7363.html'}) # Новости. Коротко (последний выпуск)
    add_item('Избранные программы', {'mode':'programs'}, fanart=fanart, isFolder=True)
    add_item('Эфиры', {'mode':'program', 'u':'z/17317'}, fanart=fanart, isFolder=True)
    add_item('Репортажи', {'mode':'program', 'u':'report/episodes'}, fanart=fanart, isFolder=True)
    add_item('Интервью', {'mode':'program', 'u':'interview/episodes'}, fanart=fanart, isFolder=True)
    add_item('Все видео', {'mode':'program', 'u':'z/17192'}, fanart=fanart, isFolder=True)

    xbmcplugin.endOfDirectory(handle)


def programs():
    add_item('Вечер', {'mode':'program', 'u':'vecher/episodes'}, icon=icon, fanart=fanarts['vecher/episodes'], isFolder=True)
    add_item('Главное', {'mode':'program', 'u':'glavnoe/episodes'}, icon=icon, fanart=fanarts['glavnoe/episodes'], isFolder=True)
    add_item('Реальное кино', {'mode':'program', 'u':'doc/episodes'}, icon=icon, fanart=fanarts['doc/episodes'], isFolder=True)
    add_item('Настоящий сериал', {'mode':'program', 'u':'series/episodes'}, icon=icon, fanart=fanarts['series/episodes'], isFolder=True)
    add_item('Неизвестная Россия', {'mode':'program', 'u':'unknownrussia/episodes'}, icon=icon, fanart=fanarts['unknownrussia/episodes'], isFolder=True)
    add_item('Человек на карте', {'mode':'program', 'u':'person/episodes'}, icon=icon, fanart=fanarts['person/episodes'], isFolder=True)
    add_item('Смотри в оба', {'mode':'program', 'u':'smotrivoba/episodes'}, icon=icon, fanart=fanarts['smotrivoba/episodes'], isFolder=True)
    add_item('Азия', {'mode':'program', 'u':'asia/episodes'}, icon=icon, fanart=fanarts['asia/episodes'], isFolder=True)
    add_item('Америка', {'mode':'program', 'u':'amerika/episodes'}, icon=icon, fanart=fanarts['amerika/episodes'], isFolder=True)

    xbmcplugin.endOfDirectory(handle)


def live():
    quality = addon.getSetting('LiveQuality')

    purl = stream_url[quality]
    item = xbmcgui.ListItem(path=purl)
    item.setInfo(type='video', infoLabels={'title':'Live'})

    if quality[:4] == 'Auto':
        item.setProperty('inputstreamaddon', 'inputstream.adaptive')

        if '.mpd' in purl:
            item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
            item.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
            item.setProperty('inputstream.adaptive.license_key', 'https://cwip-shaka-proxy.appspot.com/no_auth||R{SSM}|')
        
            item.setMimeType('application/dash+xml')
            item.setContentLookup(False)
        else:
            item.setProperty('inputstream.adaptive.manifest_type', 'hls')

    xbmcplugin.setResolvedUrl(handle, True, item)


def show_content(params):
    page = int(params.get('p', 0))
    url = params['u'] = urllib.unquote_plus(params['u'])

    html = get_html('%s/%s/' % (BASE_URL, url), {'p':page})

    container = common.parseDOM(html, 'div', attrs={'class':'media-block-wrap'})
    videos = common.parseDOM(container, 'a', attrs={'class':'img-wrap'})
    hrefs = common.parseDOM(container, 'a', attrs={'class':'img-wrap'}, ret="href")
    titles = common.parseDOM(container, 'a', attrs={'class':'img-wrap'}, ret="title")

    for i, video in enumerate(videos):
        img = common.parseDOM(video, 'img', ret='src')[0]

        thumb = re.sub(r'_w\w+', '_w512_r1', img)

        fan = fanarts.get(url, fanart)
        if addon.getSetting('DownloadFanart') == 'true':
            fan = re.sub(r'_w\w+', '_w1920_r1', img)

        title = common.replaceHTMLCodes(titles[i])
        href = hrefs[i]

        add_item(title, {'mode':'play', 'u':href}, thumb=thumb, fanart=fan, isPlayable=True)

    if common.parseDOM(html, 'p', attrs={'class':'buttons btn--load-more'}):
        params['p'] = page + 1
        add_item('Далее > %i' % (1 + params['p']), params, fanart=fanart, isFolder=True)


def program(params):
    show_content(params)

    xbmcplugin.endOfDirectory(handle)


def play_video(params):

    html = get_html('%s/%s' % (BASE_URL, params['u']))

    quality = addon.getSetting('VideoQuality')

    frame = re.compile('<meta content="(.+?)" name="twitter:player"').findall(html)

    html = get_html(frame[0])

    data = re.compile('data-sources="(.+?)" data-lt-on-play="').findall(html)
    data = json.loads(common.replaceHTMLCodes(data[0]))

    for video in data:
        if quality == video['DataInfo']:
            purl = video['AmpSrc']
            break
    else:
        purl = data[-1]['AmpSrc']

    item = xbmcgui.ListItem(path=purl)

    xbmcplugin.setResolvedUrl(handle, True, item)


def add_item(title, params={}, icon='', banner='', fanart='', poster='', thumb='', plot='', isFolder=False, isPlayable=False, url=None):
    if url == None: url = '%s?%s' % (sys.argv[0], urllib.urlencode(params))

    item = xbmcgui.ListItem(title, iconImage = icon, thumbnailImage = thumb)
    item.setInfo(type='Video', infoLabels={'Title': title, 'Plot': plot})

    if isPlayable:
        item.setProperty('mediatype', 'video')
        item.setProperty('isPlayable', 'true')
    
    if banner != '':
        item.setArt({'banner': banner})
    if fanart != '':
        item.setArt({'fanart': fanart})
    if poster != '':
        item.setArt({'poster': poster})
    if thumb != '':
        item.setArt({'thumb': thumb})

    xbmcplugin.addDirectoryItem(handle, url=url, listitem=item, isFolder=isFolder)


def get_params():
    param = {}
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


params = get_params()

mode = params.get('mode', '')

if mode == '':
    main_menu()

elif mode == 'live':
    live()

elif mode == 'programs':
    programs()

elif mode == 'program':
    program(params)

elif mode == 'play':
    play_video(params)

elif mode == 'cleancache':
    from tccleaner import TextureCacheCleaner as tcc
    tcc().remove_like('%currenttime.tv%', True)
