
import urllib
import json


class Video():
    '''
    Returns video info related for a youtube link
    '''
    def __init__(self, youtube_link):
        youtube_id = youtube_link[youtube_link.find("v=")+2:]
        data_url = "http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2" % youtube_id
        jsondata = json.load(urllib.urlopen(data_url))
# TODO:FIX       self.title = jsondata['entry']['title']['$t'] 
        self.title = youtube_id
        self.storyline = "Youtube Video"
        self.poster_image_url = "https://img.youtube.com/vi/" + youtube_id + "/hqdefault.jpg"
        self.trailer_youtube_url = youtube_link




        