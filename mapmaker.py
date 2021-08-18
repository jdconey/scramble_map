# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 14:58:10 2021

@author: mm16jdc
"""

import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.geoaxes
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from matplotlib.offsetbox import AnchoredText


from cartopy.io.img_tiles import OSM, Stamen, MapQuestOpenAerial, GoogleWTS

#import cartopy.io.img_tiles


from osconv import os_to_ll

from adjustText import adjust_text


class MapboxTiles(GoogleWTS):
    """
    Implement web tile retrieval from Mapbox.
    For terms of service, see https://www.mapbox.com/tos/.
    """
    def __init__(self, access_token, map_id):
        """
        Set up a new Mapbox tiles instance.
        Access to Mapbox web services requires an access token and a map ID.
        See https://www.mapbox.com/api-documentation/ for details.
        Parameters
        ----------
        access_token
            A valid Mapbox API access token.
        map_id
            An ID for a publicly accessible map (provided by Mapbox).
            This is the map whose tiles will be retrieved through this process.
        """
        self.access_token = access_token
        self.map_id = map_id
        super().__init__()

    def _image_url(self, tile):
        x, y, z = tile
        url = ('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}'
               '?access_token={token}'.format(z=z, y=y, x=x,
                                              id=self.map_id,
                                              token=self.access_token))
        return url


def map_mapbox():
    
    #this requires a Mapbox API key, which I open from the file mapbox.txt.
    
    f = open("mapbox.txt", "r")
    access_token = f.read()
    
    imagery = MapboxTiles(map_id='mapbox/outdoors-v11',  access_token=access_token)
    imagery2 = MapboxTiles(map_id='mapbox/outdoors-v10',  access_token=access_token)
    zoom = 11
    zoom2 = 13
    return imagery,imagery2,zoom,zoom2

def map_stamen():
    imagery=Stamen(style='terrain', desired_tile_form='RGB')
    imagery2 =Stamen(style='terrain',desired_tile_form='RGB')#, user_agent='CartoPy/0.18.0')
    zoom = 12
    zoom2 = 14
    return imagery,imagery2,zoom,zoom2


dat = pd.read_csv('gsmith.csv')

locs = dat['Grid Ref']
lats,lons=[],[]
ids = []
grade = []
colours=[]
for row in dat.iterrows():
    gridref = row[1]['Grid Ref']
    nid = row[1]['ID']
    grade = row[1]['Grade']
    
    lat, lon = os_to_ll((2000+(int(gridref[3:6])))*100,(3000+float(gridref[7:]))*100)
    lats.append(lat)
    lons.append(lon)
    ids.append(nid)
    grade=str(grade)
    if grade[0]=='1':
        colours.append('green')
    elif grade[0]=='2':
        colours.append('blue')
    elif grade[0]=='3':
        colours.append('red')
    else:
        print('oops')


fig = plt.figure(figsize=(12,8))


imagery,imagery2,zoom,zoom2 = map_mapbox()
#imagery,imagery2,zoom,zoom2 = map_stamen()

ax = fig.add_subplot(1,1,1, projection=imagery.crs)

fontsize=14

ax.add_image(imagery, 11)
ax.set_extent((min(lons)-0.01,max(lons)+0.01,min(lats)-0.005,max(lats)+0.005),crs=ccrs.PlateCarree())

rect = patches.Rectangle((lons[23]-0.0005, lats[21]-0.00025), lons[11]-lons[23]+0.0015, lats[11]-lats[21]+0.00075, linewidth=1, edgecolor='k', facecolor='none',transform=ccrs.PlateCarree())

# Add the patch to the Axes
ax.add_patch(rect)

ax.add_feature(cfeature.COASTLINE, edgecolor="tomato")
ax.add_feature(cfeature.BORDERS, edgecolor="tomato")
#ax.gridlines()

tryfani=[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
tryfan=[]
for k in tryfani:
    tryfan.append([lons[k],lats[k],colours[k],ids[k]])
    
glyderi=[34,27,28,29,30,39]


#plt.scatter(lons, lats, transform=ccrs.PlateCarree())
i=0
transform =   ccrs.PlateCarree()._as_mpl_transform(ax)
texts = []
while i<len(lats):
    
#    texts.append(ax.text(lons[i], lats[i], ids[i],transform=ccrs.PlateCarree()))
    
    if i not in tryfani and i not in glyderi:
        ax.plot(lons[i], lats[i], color=colours[i], marker='o', linestyle='', markersize=2,transform=ccrs.PlateCarree())
        ax.annotate(ids[i], (lons[i], lats[i]), fontsize=fontsize,xycoords=transform)
    if i in glyderi:
        ax.plot(lons[i], lats[i], color=colours[i], marker='o', linestyle='', markersize=2,transform=ccrs.PlateCarree())
    i=i+1

ax.annotate(ids[34], (lons[34], lats[34]-0.0015), fontsize=fontsize,xycoords=transform)
ax.annotate(ids[39], (lons[39], lats[39]-0.001), fontsize=fontsize,xycoords=transform)
ax.annotate('28-31', (lons[30]-0.0025, lats[30]+0.001), fontsize=fontsize,xycoords=transform)


axins = inset_axes(ax, width="40%", height="50%", loc="upper left", 
                   axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                   axes_kwargs=dict(map_projection=imagery.crs))#cartopy.crs.PlateCarree()))
axins.add_image(imagery2, 13)
axins.set_extent((lons[23]-0.0005,lons[11]+0.003,lats[21]-0.00025,lats[11]+0.001),crs=ccrs.PlateCarree())
i=0
transform2 =   ccrs.PlateCarree()._as_mpl_transform(axins)

while i<len(tryfan):
    ax.plot(tryfan[i][0], tryfan[i][1], color=tryfan[i][2], marker='o', linestyle='', markersize=2,transform=ccrs.PlateCarree())
    axins.plot(tryfan[i][0], tryfan[i][1], color=tryfan[i][2], marker='o', linestyle='', markersize=2,transform=ccrs.PlateCarree())
#    texts.append(ax.text(lons[i], lats[i], ids[i],transform=ccrs.PlateCarree()))
    if tryfan[i][3] not in [5,6,7,8,9,10,11,17,20]: 
        axins.annotate(tryfan[i][3], (tryfan[i][0], tryfan[i][1]), fontsize=fontsize,xycoords=transform2)
    i=i+1

axins.annotate(' 5-11', (tryfan[2][0], tryfan[2][1]+0.0008), fontsize=fontsize,xycoords=transform2)
axins.annotate('17',(tryfan[13][0]-0.001, tryfan[13][1]), fontsize=fontsize,xycoords=transform2)
axins.annotate('20',(tryfan[16][0]-0.001, tryfan[16][1]), fontsize=fontsize,xycoords=transform2)

#adjust_text(texts)

#summits - useful for Stamen Map but not necessary for Mapbox
#ax.plot(-4.076231,53.068497,  color='k', marker='^',linestyle='',markersize=5,transform=ccrs.PlateCarree())
#ax.annotate('Snowdon/Yr Wyddfa',(-4.076231-0.047,53.068497), fontsize=fontsize,xycoords=transform)

#ax.plot(-4.02978,53.10097,  color='k', marker='^',linestyle='',markersize=5,transform=ccrs.PlateCarree())
#ax.annotate('Glyder Fawr',(-4.02978+0.002,53.10097-0.001), fontsize=fontsize,xycoords=transform)

#ax.plot( -4.002055,53.147287,  color='k', marker='^',linestyle='',markersize=5,transform=ccrs.PlateCarree())
#ax.annotate('Carnedd Dafydd',(-4.002055+0.002,53.147287-0.001), fontsize=fontsize,xycoords=transform)

#ax.plot(-4.076328, 53.074989,  color='k', marker='^',linestyle='',markersize=5,transform=ccrs.PlateCarree())
#ax.annotate('Garnedd Ugain',(-4.076328-0.035, 53.074989), fontsize=fontsize,xycoords=transform)


#Map tiles from \href{http://stamen.com}{Stamen Design}, under \href{http://creativecommons.org/licenses/by/3.0}{CC BY 3.0}. Data by \href{http://openstreetmap.org}{OpenStreetMap}, under \href{http://www.openstreetmap.org/copyright}{ODbL}.



#text2 = AnchoredText('North Wales Scrambles by Garry Smith \nMap tiles \u00A9 Stamen Design, under CC BY 3.0\nMap data \u00A9 OpenStreetMap contributors, under ODbL\nMap compiled by J Coney 2021',
#                        loc=4, prop={'size': 12}, frameon=True)

text2 = AnchoredText('North Wales Scrambles by Garry Smith \nMap tiles \u00A9 Mapbox \nMap data \u00A9 OpenStreetMap contributors\nMap compiled by J Coney 2021',
                        loc=4, prop={'size': 12}, frameon=True)
ax.add_artist(text2)

plt.tight_layout()
plt.savefig('scrambles_summits2.pdf')