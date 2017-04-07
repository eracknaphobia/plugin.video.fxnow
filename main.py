from resources.lib.globals import *

params=get_params()
url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass


if mode==None:                    
    mainMenu()

elif mode==200:
    listShows()

elif mode==201:
    listSeasons()

elif mode==202:
    listEpisodes(show_id,season)
    
elif mode==300:
    listMovies()

elif mode==500:
    getStream(url)

elif mode==999:
	deauthorize()

xbmcplugin.endOfDirectory(addon_handle)