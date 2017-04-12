from resources.lib.globals import *

params=get_params()
url=None
name=None
mode=None
show_code=None
seasons=None

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
try:
    show_code=urllib.unquote_plus(params["show_code"])
except:
    pass
try:
    seasons=urllib.unquote_plus(params["seasons"])
except:
    pass


if mode==None:                    
    mainMenu()

elif mode==200:
    listShows()

elif mode==201:
    listSeasons(show_code,seasons)

elif mode==202:
    listEpisodes(show_code,season)
    
elif mode==300:
    listMovies()

elif mode==500:
    getStream(url)

elif mode==999:
	deauthorize()

xbmcplugin.endOfDirectory(addon_handle)