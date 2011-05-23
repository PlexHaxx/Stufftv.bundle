####################################################################################################

VIDEO_PREFIX = "/video/stufftv"

NAME = L('Title')

ART = 'art-default.jpg'
ICON = 'icon-default.png'

BASE_URL = "http://www.stuff.tv"
VIDCASTS_URL = "http://www.stuff.tv/video/vidcasts"
VIDEO_REVIEWS_URL = "http://www.stuff.tv/video/reviews"

####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():
    
    # Initialize the plugin
    Plugin.AddPrefixHandler(VIDEO_PREFIX, MainMenu, L('Title'), ICON, ART)
    Plugin.AddViewGroup("Basic", viewMode = "InfoList", mediaType = "items")
    Plugin.AddViewGroup("Basic", viewMode = "List", mediaType = "items")
    
    # Setup the artwork associated with the plugin
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

# This main function will setup the displayed items. This will depend if the user is currently
# logged in.
def MainMenu():
    dir = MediaContainer(disabledViewModes=["Coverflow"], title1 = L('Title'))
               
    # Movies
    dir.Append(Function(
        DirectoryItem(
            VidCastMenu,
            L('VidCasts'))))
    
    # TV Shows
    dir.Append(Function(
        DirectoryItem(
            VideoReviewMenu,
            L('Video Reviews'))))
    
    return dir

####################################################################################################
# VIDCASTS
####################################################################################################

def VidCastMenu(sender, url = VIDCASTS_URL):
    dir = MediaContainer(disabledViewModes=["Coverflow"], title1 = L('Title')) 

    vidcasts_page = HTML.ElementFromURL(url)
    vidcasts = vidcasts_page.xpath("//div[@class='item-list']/ul/li[@class='product']")
    
    for item in vidcasts:
        
         try:

             # Attempt to determine the title
             title = item.xpath(".//h4/a/text()")[0]

             # Attempt to determine the absolue URL to the page
             relative_url = item.xpath(".//div/a")[0].get('href')
             url = BASE_URL + String.Quote(relative_url)
             Log(url)

             # [Optional] - Attempt to determine the subtitle
             subtitle = None
             try: subtitle = item.xpath(".//p[@class='meta']/text()")[0]
             except: pass

             # [Optional] - Attempt to determine the thumbnail
             thumb = None
             try: thumb = item.xpath(".//div/a/img")[0].get('src')
             except: pass

             dir.Append(WebVideoItem(
                 url,
                 title = title,
                 subtitle = subtitle,
                 thumb = thumb))

         except:
             pass

    try:

        # Attempt to determine if there is more videos available on the next page.
        next_relative_url = vidcasts_page.xpath("//div[@class='pagination']/span[@class='next']/a[@class='active']")[0].get('href')
        next_url = BASE_URL + String.Quote(next_relative_url)

        dir.Append(Function(DirectoryItem(
            VidCastMenu,
            "Next"),
            url = next_url))

    except: 
        pass

    return dir

####################################################################################################
# VIDEO REVIEWS
####################################################################################################

def VideoReviewMenu(sender, url = VIDEO_REVIEWS_URL):
    dir = MediaContainer(disabledViewModes=["Coverflow"], title1 = L('Title')) 

    video_reviews_page = HTML.ElementFromURL(url)
    video_reviews = video_reviews_page.xpath("//div[@class='item-list']/ul/li[@class='product']")

    for item in video_reviews:

         try:

             # Attempt to determine the title
             title = item.xpath(".//h4/a/text()")[0]

             # Attempt to determine the absolue URL to the page
             relative_url = item.xpath(".//div/a")[0].get('href')
             url = BASE_URL + String.Quote(relative_url)

             # [Optional] - Attempt to determine the subtitle
             subtitle = None
             try: subtitle = item.xpath(".//p[@class='meta']/text()")[0]
             except: pass

             # [Optional] - Attempt to determine the thumbnail
             thumb = None
             try: thumb = item.xpath(".//div/a/img")[0].get('src')
             except: pass

             dir.Append(WebVideoItem(
                 url,
                 title = title,
                 subtitle = subtitle,
                 thumb = thumb))

         except:
             pass

    try:

        # Attempt to determine if there is more videos available on the next page.
        next_relative_url = vidcasts_page.xpath("//div[@class='pagination']/span[@class='next']/a[@class='active']")[0].get('href')
        next_url = BASE_URL + String.Quote(next_relative_url)

        dir.Append(Function(DirectoryItem(
            VidCastMenu,
            "Next"),
            url = next_url))

    except: 
        pass

    return dir