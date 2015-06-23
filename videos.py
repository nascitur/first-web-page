
import urllib2
import json


class Video():
    '''
    Returns video info related for a youtube link
    '''
    def __init__(self, youtube_link):
        linkapi = "http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json"
        imgapi = "https://img.youtube.com/vi/%s/hqdefault.jpg"
        try:
            youtube_id = youtube_link[youtube_link.find("v=")+2:]
            data_url = linkapi % youtube_id
#            jsondata = json.load(urllib2.urlopen(data_url))
# TODO:FIX          self.title = jsondata['entry']['title']['$t'] 
            self.title = youtube_id
            self.storyline = "Youtube Video"
            self.poster_image_url = imgapi % youtube_id
            self.trailer_youtube_url = youtube_link
            print youtube_link
        except IOError:
            print "No Internet Connection"
            self.title = youtube_link
            self.storyline = "Youtube Video"
            self.poster_image_url = "images/turkey.png"
            self.trailer_youtube_url = youtube_link     




        