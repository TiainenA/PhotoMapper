import os
import shutil

from PIL import Image
import piexif
from GPSPhoto import gpsphoto

from geopy.geocoders import GeoNames #For naming the coordinates. Optional feature
from userSpecifics import geonames_username, geonames_falseusername#git ignored
geo = GeoNames(username=geonames_username)


from pprint import pprint #For debugging only

#global-ish variables
imageLongSide=600
imageShortSide=400

class photo:
    def __init__(self, path):
        self._path=path
        self._location=gpsphoto.getGPSData(self._path)
        self._img=Image.open(self._path)
        self._exif = self._exif_to_tag(piexif.load(self._img.info.get('exif')))
        self._locationText=self._reverseGeo()
        self._formResizePath()
        self._resize()
    
    @property
    def locationText(self):
        """I'm the 'locationText' property."""
        return self._locationText

    @locationText.setter
    def locationText(self, value):
        self._locationText = value

    @property
    def location(self):
        """I'm the 'location' property."""
        return self._location
    @property
    def exif(self):
        """I'm the 'exif' property."""
        return self._exif
    @property
    def path(self):
        """I'm the 'path' property."""
        return self._path
    @property
    def resizepath(self):
        """I'm the 'resizepath' property."""
        return self._resizepath
   
    def _formResizePath(self):
        head, tail = os.path.split(self._path)

        if not os.path.exists(os.path.join(head,"resize")):
            os.mkdir(os.path.join(head,"resize"))

            
        value=os.path.join(head,"resize","resize"+tail)
        print(value)
            
        self._resizepath = value
    def _resize(self):
        if self.exif['Exif']['PixelXDimension']> self.exif['Exif']['PixelYDimension']:
            resizeWidth=imageLongSide
            resizeHeight=imageShortSide
        elif self.exif['Exif']['PixelXDimension']< self.exif['Exif']['PixelYDimension']:
            resizeWidth=imageShortSide
            resizeHeight=imageLongSide
        else:
            resizeWidth=imageShortSide
            resizeHeight=imageShortSide
            
        smallimage = self._img.resize((resizeWidth, resizeHeight), Image.ANTIALIAS)

        smallimage.save(self._resizepath, quality=100)


    def _exif_to_tag(self,exif_dict):
        codec = 'ISO-8859-1'  # or latin-1
        exif_tag_dict = {}
        thumbnail = exif_dict.pop('thumbnail')
        exif_tag_dict['thumbnail'] = thumbnail.decode(codec)

        for ifd in exif_dict:
            exif_tag_dict[ifd] = {}
            for tag in exif_dict[ifd]:
                try:
                    element = exif_dict[ifd][tag].decode(codec)

                except AttributeError:
                    element = exif_dict[ifd][tag]

                exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

        return exif_tag_dict

    def _reverseGeo(self):
        try:
            palautettava=geo.reverse(query=(self._location['Latitude'], self._location['Longitude']), exactly_one=False, timeout=5)
        except:
            palautettava=[(f"Location {self._location['Latitude']},{self._location['Longitude']}")]
        return(palautettava)


class photoFolder:
    def __init__(self,folderName):
        
        self._folderName=folderName
        self._remove_resizes(folderName)

        self.imageDict=self.list_images(folderName)
    
    @property
    def folderName(self):
        """I'm the 'folderName' property."""
        return self._folderName


    def _remove_resizes(self, kansio):
        resizePath=os.path.join(os.getcwd(),kansio,"resize")
        if os.path.exists(resizePath):
            shutil.rmtree(resizePath)


    def list_images(self,kansio):

        KuvaKansio=os.path.join(os.getcwd(),kansio)
        KuvaLista =os.listdir(KuvaKansio)
        KuvaPolut=[]
        for filename in KuvaLista:
            KuvaPolut.append(os.path.join(KuvaKansio, filename))
        palautettava={}
        for kuva in KuvaLista:
                for polku in KuvaPolut:
                    palautettava[kuva] = photo(polku)
                    KuvaPolut.remove(polku)
                    break

        return(palautettava)
    
        





def main():
    kuvat=photoFolder('kuva')
    
    print(kuvat.imageDict.keys())
    for x in kuvat.imageDict.keys():
        
         pprint(x)
         pprint(kuvat.imageDict[x].location)
    #     pprint(kuvat.imageDict[x].location['UTC-Time'])
    #     pprint(kuvat.imageDict[x].resizepath)
         pprint(kuvat.imageDict[x].exif)
         pprint(kuvat.imageDict[x].exif['Exif']['PixelXDimension'])
    #     pprint(kuvat.imageDict[x].locationText[0])
    #     kuvat.imageDict[x].locationText[0]="hattu"
    #     pprint(kuvat.imageDict[x].locationText[0])        
    
    #print(list(kuvat.imageDict.keys())[0])


    


if __name__ == "__main__":
    main()