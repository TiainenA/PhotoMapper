import folium
from folium import IFrame
import base64

import pm_photos

def setbounds(folder:pm_photos.photoFolder):
    bounds={}
    lats=[]
    longs=[]


    for photo in folder.imageDict.values():
        lats.append(photo.location['Latitude'])
        longs.append(photo.location['Longitude'])
    bounds["north"]=max(lats)
    bounds["south"]=min(lats)
    bounds["east"]=max(longs)
    bounds["west"]=min(longs)
    return(bounds)



def addPhotosToMap(map:folium.Map, folder:pm_photos.photoFolder):
    for photo in folder.imageDict.values():
        if photo.exif['Exif']['PixelXDimension']> photo.exif['Exif']['PixelYDimension']:
            resizeWidth=pm_photos.imageLongSide
            resizeHeight=pm_photos.imageShortSide
        elif photo.exif['Exif']['PixelXDimension']< photo.exif['Exif']['PixelYDimension']:
            resizeWidth=pm_photos.imageShortSide
            resizeHeight=pm_photos.imageLongSide
        else:
            resizeWidth=pm_photos.imageShortSide
            resizeHeight=pm_photos.imageShortSide
        html = '<img src="data:image/jepg;base64,{}">'.format
    
        encoded = base64.b64encode(open(photo.resizepath, 'rb').read())
        iframe = IFrame(html(encoded.decode('UTF-8')), width=resizeWidth+20, height=resizeHeight+20)
        popup = folium.Popup(iframe, max_width=resizeWidth+100)
        icon = folium.Icon(color="red", icon="ok")
        folium.Marker(location=[photo.location['Latitude'],photo.location['Longitude']], popup=popup, tooltip=photo.locationText[0], icon=icon).add_to(map)

    
    return(map)



def main():
    kuvaKansio=pm_photos.photoFolder('kuva')
    
    bounds=setbounds(kuvaKansio)

    kartta=folium.Map(tiles="Stamen Terrain")
    addPhotosToMap(kartta,kuvaKansio)
     
    kartta.fit_bounds([[bounds['south'],bounds['west']],[bounds['north'],bounds['east']]])
    folium.LayerControl().add_to(kartta)	



    kartta.save("index.html")


if __name__ == "__main__":
    main()