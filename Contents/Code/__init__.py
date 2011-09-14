####################################################################################################

VIDEO_PREFIX = "/video/stufftv"

NAME = L('Title')

ART = 'art-default.jpg'
ICON = 'icon-default.png'
ICON_SEARCH = 'icon-search.png'

BASE_URL = "http://www.stuff.tv"
VIDCASTS_URL = "http://www.stuff.tv/video/vidcasts"
VIDEO_REVIEWS_URL = "http://www.stuff.tv/video/reviews"
SEARCH_URL = "http://www.stuff.tv/search/video?search=%s"

####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():
    
    # Initialize the plugin
    Plugin.AddPrefixHandler(VIDEO_PREFIX, MainMenu, L('Title'), ICON, ART)
    Plugin.AddViewGroup("List", viewMode = "List", mediaType = "items")
    
    # Set the default ObjectContainer attributes
    ObjectContainer.title1 = NAME
    ObjectContainer.view_group = 'List'
    ObjectContainer.art = R(ICON)

    # Default icons for DirectoryObject, VideoClipObject and SearchDirectoryObject in case there isn't an image
    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)
    SearchDirectoryObject.thumb = R(ICON)
    SearchDirectoryObject.art = R(ART)

    # Cache HTTP requests for up to a day
    HTTP.CacheTime = CACHE_1DAY

def MainMenu():
    oc = ObjectContainer(title1 = L('Title'))

    oc.add(DirectoryObject(key = Callback(VidCastMenu), title = L('VidCasts')))
    oc.add(DirectoryObject(key = Callback(VideoReviewMenu), title = L('VideoReviews')))
    oc.add(SearchDirectoryObject(identifier="com.plexapp.search.stufftv", title = L('Search'), prompt = L('SearchPrompt'), thumb = R(ICON)))

    return oc

####################################################################################################
# VIDCASTS
####################################################################################################

def VidCastMenu(url = VIDCASTS_URL):
    oc = ObjectContainer(title1 = L('Title'), title2 = L('VidCasts')) 

    vidcasts_page = HTML.ElementFromURL(url)
    vidcasts_initial_node = vidcasts_page.xpath("//div[@class='inner-container']/div/h2[contains(text(), 'Vidcasts')]/..")[0]
    vidcasts = vidcasts_initial_node.xpath(".//div[@class='item-list']/ul/li//div[contains(@class,'product')]")
    
    for item in vidcasts:
        
         try:

             # Attempt to determine the title
             title = item.xpath(".//h4/a/text()")[0]

             # Attempt to determine the absolue URL to the page
             relative_url = item.xpath(".//div/a")[0].get('href')
             url = BASE_URL + String.Quote(relative_url)

             # [Optional] - Attempt to determine the date
             date = None
             try: 
                 date = item.xpath(".//p[@class='meta']/text()")[0]
                 date = Datetime.ParseDate(date)
             except: pass

             # [Optional] - Attempt to determine the thumbnail
             thumb = None
             try: 
                 thumb_url = item.xpath(".//div/a/img")[0].get('src')
                 thumb = "http:" + String.Quote(thumb_url[5:])
             except: pass

             oc.add(VideoClipObject(
                 url = url,
                 title = title,
                 thumb = thumb,
                 originally_available_at = date))

         except:
             pass

    try:

        # Attempt to determine if there is more videos available on the next page.
        next_relative_url = vidcasts_page.xpath("//div[@class='pagination']/span[@class='next']/a[@class='active']")[0].get('href')
        next_url = BASE_URL + next_relative_url
        oc.add(DirectoryObject(key = Callback(VidCastMenu, url = next_url), title = L('Next')))

    except: 
        pass

    return oc

####################################################################################################
# VIDEO REVIEWS
####################################################################################################

def VideoReviewMenu(url = VIDEO_REVIEWS_URL):
    oc = ObjectContainer(title1 = L('Title'), title2 = L('VideoReviews')) 
    
    video_reviews_page = HTML.ElementFromURL(url)
    video_reviews_initial_node = video_reviews_page.xpath("//div[@class='inner-container']/div/h2[contains(text(), 'Video reviews')]/..")[0]
    video_reviews = video_reviews_initial_node.xpath(".//div[@class='item-list']/ul/li//div[contains(@class,'product')]")

    for item in video_reviews:

         try:

             # Attempt to determine the title
             title = item.xpath(".//h4/a/text()")[0]

             # Attempt to determine the absolue URL to the page
             relative_url = item.xpath(".//div/a")[0].get('href')
             url = BASE_URL + String.Quote(relative_url)

             # [Optional] - Attempt to determine the subtitle
             date = None
             try: 
                 date = item.xpath(".//p[@class='meta']/text()")[0]
                 date = Datetime.ParseDate(date)
             except: pass

             # [Optional] - Attempt to determine the thumbnail
             thumb = None
             try: 
                 thumb_url = item.xpath(".//div/a/img")[0].get('src')
                 thumb = "http:" + String.Quote(thumb_url[5:])
             except: pass

             oc.add(VideoClipObject(
                 url = url,
                 title = title,
                 thumb = thumb,
                 originally_available_at = date))

         except:
             pass

    try:

        # Attempt to determine if there is more videos available on the next page.
        next_relative_url = video_reviews_page.xpath("//div[@class='pagination']/span[@class='next']/a[@class='active']")[0].get('href')
        next_url = BASE_URL + next_relative_url
        oc.add(DirectoryObject(key = Callback(VideoReviewMenu, url = next_url), title = L('Next')))

    except: 
        pass

    return oc