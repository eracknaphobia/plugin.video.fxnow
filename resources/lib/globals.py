import sys, os
import xbmc, xbmcplugin, xbmcgui, xbmcaddon
import urllib, urllib2
import json
import base64
from adobepass.adobe import ADOBE


addon_handle = int(sys.argv[1])
ADDON = xbmcaddon.Addon()
ROOTDIR = ADDON.getAddonInfo('path')
FANART = os.path.join(ROOTDIR,"resources","fanart.jpg")
ICON = os.path.join(ROOTDIR,"resources","icon.png")


#Addon Settings 
RATIO = str(ADDON.getSetting(id="ratio"))
COMMENTARY = str(ADDON.getSetting(id="commentary"))
LOCAL_STRING = ADDON.getLocalizedString

RESOURCE_ID = "<rss version='2.0'><channel><title>fx</title></channel></rss>"
UA_FX = 'FXNOW/1135 CFNetwork/808.3 Darwin/16.3.0'
AUTH = 'androidtv:a4y4o0e01jh27dsyrrgpvo6d1wvpravc2c4szpp4'

#Add-on specific Adobepass variables
SERVICE_VARS = {'app_version': 'Fire TV',
                'device_type':'firetv',             
                'private_key':'B081JNlGKn1ZqpQH',
                'public_key':'Dy1OhW3HrWk03QJrMMIULAmUdPQqk2Ds',
                'registration_url':'fxnetworks.com/activate',
                'requestor_id':'fx',
                'resource_id':urllib.quote(RESOURCE_ID)
               }

def mainMenu():
    #addDir('Featured','/movies',100,ICON)
    addDir('Shows',200,ICON)
    addDir('Movies',300,ICON)
    #addDir('Live TV','/tv',400,ICON)


def listMovies():
    url = 'http://fapi2.fxnetworks.com/ios/videos'
    url += '?fields=guid,canonical,featuredReason,featuredWeight,fullEpisode,genre,houseNumber,movie,network,name,original,premiere,promoteMovie,season,source,stage,type,uID,dialogue,slug,longDescription,episode,showcode,_id,aptve_video_url,fapi_show_id,ingest_id,ios_video_url,is_live,mobile_video_url,movie_clip,mpxId,requiresAuth,freewheelId,sami_url,scc_url,show_id,srt_url,video_url,year_released,delivery_format,description,img_url,airDate,authEndDate,availableDate,bankableAvailableDate,bankableExpirationDate,expirationDate,displayAvailableDate,displayExpirationDate,endDate,duration,series_title,video_urls,win8VideoRow,images,ratings,categories,tags,actors,guestStars,actors,majorCharacters,video_url_commentary,factoids,videos,freewheelId_commentary,trailerGUID&order=airDate:desc&filter%5Btype%5D=movie%7Cmovie-trailer&limit=500'
    #url += '?fields=movie&limit=500'
    json_source = jsonRequest(url)

    for show in json_source['videos']:
        name = show['name']
        if 'TRAILER:' not in name:
            icon = show['images']['poster_2x3']
            fanart = FANART
            if 'thumbnail_16x9' in show['images']: fanart = show['images']['thumbnail_16x9']
            url = show['ios_video_url']
            #addStream(name,link_url,title,iconimage,fanart,info=None)
            addStream(name,url,name,icon,fanart)



def listLiveTV(): 
    url = "http://fapi2.fxnetworks.com/ios/videos?fields=guid,canonical,featuredReason,featuredWeight,fullEpisode,genre,houseNumber,movie,network,name,original,premiere,promoteMovie,season,source,stage,type,uID,dialogue,slug,longDescription,episode,showcode,_id,aptve_video_url,fapi_show_id,ingest_id,ios_video_url,is_live,mobile_video_url,movie_clip,mpxId,requiresAuth,freewheelId,sami_url,scc_url,show_id,srt_url,video_url,year_released,delivery_format,description,img_url,airDate,authEndDate,availableDate,bankableAvailableDate,bankableExpirationDate,expirationDate,displayAvailableDate,displayExpirationDate,endDate,duration,series_title,video_urls,win8VideoRow,images,ratings,categories,tags,actors,guestStars,actors,majorCharacters,video_url_commentary,factoids,videos,freewheelId_commentary,trailerGUID&order=airDate:desc&filter%5Btype%5D=movie%7Cmovie-trailer&limit=500"
    json_source = jsonRequest(url)

    for show in json_source['videos']:
        name = show['name']
        if 'TRAILER:' not in name:
            icon = show['images']['poster_2x3']
            fanart = show['images']['thumbnail_16x9']
            url = show['ios_video_url']
            addStream(name,url,201,icon,fanart)



def listShows():
    url = "http://fapi2.fxnetworks.com/ios/shows"
    url += "?limit=500&fields=_id,availability_message,available_date,featured_reason,featured_weight,genre,hashtag,original,name,season,showcode,network,seasons,mega_og_description,meta_description,forum_page,social_facebook,social_getglue,social_twitter,tagline,tunein_text,sunrise,sunset,latest_playable_episode,latest_playable_clip,images,meta_keywords"        
    json_source = jsonRequest(url)
    for show in json_source['shows']:
        name = show['name']
        meta_desc = show['meta_description']
        genre = show['genre']
        icon = show['images']['poster_2x3']
        fanart = ''
        if 'thumbnail_16x9' in show['images']: fanart = show['images']['series_menu_4x3']
        show_code = show['showcode']
        seasons = ''
        for season in show['seasons']:            
            if seasons != '': seasons += ','            
            seasons += str(season)

        info = {'plot':meta_desc,'tvshowtitle':name,'title':name,'originaltitle':name,'genre':genre}

        if seasons != '':
            addDir(name,201,icon,fanart,info,show_code,seasons)


def listSeasons(show_code,seasons,icon,fanart):          
    #if only more than one seasons list else list episodes of season
    if ',' in seasons:
        for season in seasons.split(','):
            addDir('Season '+str(season),201,icon,fanart,None,show_code,season)
    else:
        listEpisodes(show_code,seasons)

    
def listEpisodes(show_code,season):    
    url = "http://fapi2.fxnetworks.com/androidtv/videos"
    url += "?filter%5Bshowcode%5D="+show_code
    url += "&filter%5Bseason%5D="+season+"&limit=500&filter%5Btype%5D=episode"    
    json_source = jsonRequest(url)
    
    #for episode in reversed(json_source['videos']):            
    for episode in sorted(json_source['videos'], key=lambda k: k['episode']):
        show_title = episode['tags'][0]
        title = episode['name']        
        genre = episode['genre']
        #Default video type is 16x9
        link_url = episode['androidtv_video_url']
        icon = episode['img_url']
        desc = episode['description']
        duration = episode['duration']
        aired = episode['airDate']
        season = str(episode['season']).zfill(2) 
        episode = str(episode['episode']).zfill(2)         

        info = {'plot':desc,'tvshowtitle':show_title, 'season':season, 'episode':episode, 'title':title,'originaltitle':title,'duration':duration,'aired':aired,'genre':genre}
        
        #addEpisode(title,url,title,icon,FANART,info)
        addStream(title,link_url,title,icon,None,info)



def getStream(url):
    adobe = ADOBE(SERVICE_VARS)            
    if adobe.checkAuthN():
        if adobe.authorize():
            media_token = adobe.mediaToken()    
            #url = url.replace('SMIL','redirect')   
            url += '&formt=redirect'
            url += "&auth="+urllib.quote(base64.b64decode(media_token))
            req = urllib2.Request(url)
            req.add_header("Accept", "*/*")
            req.add_header("Accept-Encoding", "deflate")
            req.add_header("Accept-Language", "en-us")
            req.add_header("Connection", "keep-alive")        
            req.add_header("User-Agent", UA_FX)
            response = urllib2.urlopen(req)              
            source = response.read()
            response.close() 

            #get the last url forwarded to
            stream_url = response.geturl()
            if '.m3u8' not in stream_url :
                stream_url = findString(source,'<video src="','"')
                
            stream_url = stream_url + '|User-Agent=okhttp/3.4.1'            
            listitem = xbmcgui.ListItem(path=stream_url)
            xbmcplugin.setResolvedUrl(addon_handle, True, listitem)
        else:
            sys.exit()
    else:
        #msg = 'Your device\'s is not currently authorized to view the selected content.\n Would you like to authorize this device now?'
        dialog = xbmcgui.Dialog() 
        answer = dialog.yesno(LOCAL_STRING(30911), LOCAL_STRING(30910))
        if answer:
            adobe.registerDevice()
            getStream(url)
        else:
            sys.exit()


def jsonRequest(url):
    req = urllib2.Request(url)
    req.add_header("Connection", "keep-alive")
    req.add_header("Accept", "*/*")
    req.add_header("Accept-Encoding", "deflate")
    req.add_header("Accept-Language", "en-us")
    req.add_header("Connection", "keep-alive")
    req.add_header("Authentication", AUTH)
    req.add_header("User-Agent", UA_FX)
    response = urllib2.urlopen(req)   
    json_source = json.load(response)                       
    response.close() 

    return json_source


def findString(source,start_str,end_str):    
    start = source.find(start_str)
    end = source.find(end_str,start+len(start_str))

    if start != -1:        
        return source[start+len(start_str):end]
    else:
        return ''


def deauthorize():
    adobe = ADOBE(SERVICE_VARS)
    adobe.deauthorizeDevice()
    dialog = xbmcgui.Dialog()      
    dialog.notification(LOCAL_STRING(30900), LOCAL_STRING(30901), '', 5000, False)  
        

def addDir(name,mode,icon,fanart=None,info=None,show_code=None,seasons=None): 
    params = get_params()      
    ok=True    
    u=sys.argv[0]+"?mode="+str(mode)+'&icon='+urllib.quote_plus(icon)
    if show_code != None: u += '&show_code='+str(show_code)
    if seasons != None: u += '&seasons='+str(seasons)
    if fanart != None: u += '&fanart='+urllib.quote_plus(fanart)

    liz=xbmcgui.ListItem(name)
    liz.setArt({'icon': ICON, 'thumb': icon, 'fanart': fanart})    
    if info != None:
        liz.setInfo( type="Video", infoLabels=info)     
    ok=xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=True)    
    xbmcplugin.setContent(addon_handle, 'tvshows')
    return ok


def addStream(name,link_url,title,iconimage,fanart,info=None):
    ok=True
    u=sys.argv[0]+"?url="+urllib.quote_plus(link_url)+"&mode="+str(500)
    liz=xbmcgui.ListItem(name)
    liz.setArt({'icon': ICON, 'thumb': iconimage, 'fanart': fanart})    
    liz.setProperty("IsPlayable", "true")
    liz.setInfo( type="Video", infoLabels={ "Title": title, 'mediatype': 'episode' } )
    if info != None:
        liz.setInfo( type="Video", infoLabels=info) 
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    xbmcplugin.setContent(addon_handle, 'tvshows')    
    return ok


def addSeason(name,url,mode,iconimage,fanart=None,info=None): 
    params = get_params()      
    ok=True    
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name)
    liz.setArt({'icon': ICON, 'thumb': iconimage, 'fanart': fanart})
    liz.setInfo( type="Video", infoLabels={ 'Title': name, 'tvdb_id': '71663', 'mediatype': 'season' } )
    if info != None:
        liz.setInfo( type="Video", infoLabels=info)     
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)    
    xbmcplugin.setContent(addon_handle, 'tvshows')
    return ok


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                    params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                    splitparams={}
                    splitparams=pairsofparams[i].split('=')
                    if (len(splitparams))==2:
                            param[splitparams[0]]=splitparams[1]
                            
    return param