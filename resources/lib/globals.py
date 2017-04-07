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
    #addDir('Shows','/movies',200,ICON)
    addDir('Movies','/tv',300,ICON)
    #addDir('Live TV','/tv',400,ICON)


def listShows():

    url = "http://fapi2.fxnetworks.com/ios/shows?limit=500&fields=_id,availability_message,available_date,featured_reason,featured_weight,genre,hashtag,original,name,season,showcode,network,seasons,mega_og_description,meta_description,forum_page,social_facebook,social_getglue,social_twitter,tagline,tunein_text,sunrise,sunset,latest_playable_episode,latest_playable_clip,images,meta_keywords"    
    req = urllib2.Request(url)
    req.add_header("Connection", "keep-alive")
    req.add_header("Accept", "*/*")
    req.add_header("Accept-Encoding", "deflate")
    req.add_header("Accept-Language", "en-us")
    req.add_header("Connection", "keep-alive")
    req.add_header("Authentication", "androidtv:a4y4o0e01jh27dsyrrgpvo6d1wvpravc2c4szpp4")
    req.add_header("User-Agent", UA_FX)
    response = urllib2.urlopen(req)   
    json_source = json.load(response)                       
    response.close() 

    for show in json_source['shows']:
        name = show['name']
        xbmc.log(name)
        icon = show['images']['poster_2x3']
        fanart = ''
        if 'thumbnail_16x9' in show['images']: fanart = show['images']['thumbnail_16x9']

        addDir(name,'',201,icon,fanart)


def listMovies():

    url = "http://fapi2.fxnetworks.com/ios/videos?fields=guid,canonical,featuredReason,featuredWeight,fullEpisode,genre,houseNumber,movie,network,name,original,premiere,promoteMovie,season,source,stage,type,uID,dialogue,slug,longDescription,episode,showcode,_id,aptve_video_url,fapi_show_id,ingest_id,ios_video_url,is_live,mobile_video_url,movie_clip,mpxId,requiresAuth,freewheelId,sami_url,scc_url,show_id,srt_url,video_url,year_released,delivery_format,description,img_url,airDate,authEndDate,availableDate,bankableAvailableDate,bankableExpirationDate,expirationDate,displayAvailableDate,displayExpirationDate,endDate,duration,series_title,video_urls,win8VideoRow,images,ratings,categories,tags,actors,guestStars,actors,majorCharacters,video_url_commentary,factoids,videos,freewheelId_commentary,trailerGUID&order=airDate:desc&filter%5Btype%5D=movie%7Cmovie-trailer&limit=500"
    req = urllib2.Request(url)
    req.add_header("Connection", "keep-alive")
    req.add_header("Accept", "*/*")
    req.add_header("Accept-Encoding", "deflate")
    req.add_header("Accept-Language", "en-us")
    req.add_header("Connection", "keep-alive")
    req.add_header("Authentication", "androidtv:a4y4o0e01jh27dsyrrgpvo6d1wvpravc2c4szpp4")
    req.add_header("User-Agent", UA_FX)
    response = urllib2.urlopen(req)   
    json_source = json.load(response)                       
    response.close() 

    for show in json_source['videos']:
        name = show['name']
        if 'TRAILER:' not in name:
            icon = show['images']['poster_2x3']
            fanart = FANART
            if 'thumbnail_16x9' in show['images']:
                fanart = show['images']['thumbnail_16x9']
            url = show['ios_video_url']
            addStream(name,url,201,icon,fanart)


def listLiveTV(): 
    url = "http://fapi2.fxnetworks.com/ios/videos?fields=guid,canonical,featuredReason,featuredWeight,fullEpisode,genre,houseNumber,movie,network,name,original,premiere,promoteMovie,season,source,stage,type,uID,dialogue,slug,longDescription,episode,showcode,_id,aptve_video_url,fapi_show_id,ingest_id,ios_video_url,is_live,mobile_video_url,movie_clip,mpxId,requiresAuth,freewheelId,sami_url,scc_url,show_id,srt_url,video_url,year_released,delivery_format,description,img_url,airDate,authEndDate,availableDate,bankableAvailableDate,bankableExpirationDate,expirationDate,displayAvailableDate,displayExpirationDate,endDate,duration,series_title,video_urls,win8VideoRow,images,ratings,categories,tags,actors,guestStars,actors,majorCharacters,video_url_commentary,factoids,videos,freewheelId_commentary,trailerGUID&order=airDate:desc&filter%5Btype%5D=movie%7Cmovie-trailer&limit=500"
    req = urllib2.Request(url)
    req.add_header("Connection", "keep-alive")
    req.add_header("Accept", "*/*")
    req.add_header("Accept-Encoding", "deflate")
    req.add_header("Accept-Language", "en-us")
    req.add_header("Connection", "keep-alive")
    req.add_header("Authentication", "androidtv:a4y4o0e01jh27dsyrrgpvo6d1wvpravc2c4szpp4")
    req.add_header("User-Agent", UA_FX)
    response = urllib2.urlopen(req)   
    json_source = json.load(response)                       
    response.close() 

    for show in json_source['videos']:
        name = show['name']
        if 'TRAILER:' not in name:
            icon = show['images']['poster_2x3']
            fanart = show['images']['thumbnail_16x9']
            url = show['ios_video_url']
            addStream(name,url,201,icon,fanart)

def listSeasons(show_id):       
    for x in range(1, 29):
        title = "Season "+str(x)
        url = str(x)
        #icon = 'http://thetvdb.com/banners/seasons/71663-'+str(x)+'-15.jpg'
        #icon = 'http://thetvdb.com/banners/seasonswide/71663-'+str(x)+'.jpg'        
        #icon = 'http://thetvdb.com/banners/seasons/71663-'+str(x)+'.jpg'
        icon = art_root+season_art[str(x)]

        addSeason(title,url,101,icon,FANART)


def listEpisodes(show_id,season):    
    url = "http://fapi2.fxnetworks.com/androidtv/videos"
    url += "?filter%5Bfapi_show_id%5D="+show_id
    url += "&filter%5Bseason%5D="+season+"&limit=500&filter%5Btype%5D=episode"    
    req = urllib2.Request(url)
    req.add_header("Connection", "keep-alive")
    req.add_header("Accept", "*/*")
    req.add_header("Accept-Encoding", "deflate")
    req.add_header("Accept-Language", "en-us")
    req.add_header("Connection", "keep-alive")
    req.add_header("Authentication", "androidtv:a4y4o0e01jh27dsyrrgpvo6d1wvpravc2c4szpp4")
    req.add_header("User-Agent", UA_FX)
    response = urllib2.urlopen(req)   
    json_source = json.load(response)                       
    response.close() 
    
    #for episode in reversed(json_source['videos']):            
    for episode in sorted(json_source['videos'], key=lambda k: k['episode']):
        title = episode['name']
        #Default video type is 16x9
        url = episode['video_urls']['16x9']['en_US']['video_url']         
        try: url = episode['video_urls'][RATIO]['en_US']['video_url']
        except: pass
        if COMMENTARY == 'true':
            try: url = episode['video_urls'][RATIO]['en_US']['video_url_commentary']
            except: pass
        icon = episode['img_url']
        desc = episode['description']
        duration = episode['duration']
        aired = episode['airDate']
        season = str(episode['season']).zfill(2) 
        episode = str(episode['episode']).zfill(2)         

        info = {'plot':desc,'tvshowtitle':LOCAL_STRING(30000), 'season':season, 'episode':episode, 'title':title,'originaltitle':title,'duration':duration,'aired':aired,'genre':LOCAL_STRING(30002)}
        
        addEpisode(title,url,title,icon,FANART,info)



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
            #stream_url = response.geturl()
            xbmc.log(source)
            stream_url = findString(source,'<video src="','"')
            #stream_url = 'https://fxmhds-vh.akamaihd.net/i/video/FX_Networks_FXM_Features/830/483/Transformers_4_HD_Clean_AUTH_movie_9006638758,13_mp4_video_640x360_800000_primary_audio_eng_5_1489800626547_932291,18_mp4_video_1280x720_4500000_primary_audio_eng_10_1489800625409_4634787,17_mp4_video_1280x720_3400000_primary_audio_eng_9_1489800627591_3533017,16_mp4_video_1280x720_2500000_primary_audio_eng_8_1489800628058_2633079,15_mp4_video_1280x720_1800000_primary_audio_eng_7_1489800628631_1933185,14_mp4_video_1024x576_1300000_primary_audio_eng_6_1489800626023_1433206,12_mp4_video_480x270_500000_primary_audio_eng_4_1489800624359_632290,11_mp4_video_480x270_300000_primary_audio_eng_3_1489800627053_432312,20_mp4_video_400x0_225000_primary_audio_eng_2_1489800629084_357311,19_mp4_video_400x0_150000_primary_audio_eng_1_1489800624889_282311,.mp4.csmil/master.m3u8?hdnea=st=1491073078~exp=1491087508~acl=/i/video/FX_Networks_FXM_Features/830/483/Transformers_4_HD_Clean_AUTH_movie_9006638758*~id=b6a52a4b-04ed-44f1-8395-6531c1dbdbca~hmac=03f178f4025399da26f9379f88194ac86cb3d63b72ca75e577db7e555c7b1c33'
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
        

def addDir(name,id,mode,iconimage,fanart=None,info=None): 
    params = get_params()      
    ok=True    
    u=sys.argv[0]+"?id="+urllib.quote_plus(id)+"&mode="+str(mode)
    liz=xbmcgui.ListItem(name)
    liz.setArt({'icon': ICON, 'thumb': iconimage, 'fanart': fanart})    
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