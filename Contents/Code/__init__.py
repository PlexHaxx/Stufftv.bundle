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
    Plugin.AddPrefixHandler("/video/stufftv", MainMenu, L('Title'), ICON, ART)
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
            L('VideoReviews'))))
    
    # Search
    dir.Append(Function(
        InputDirectoryItem(
            SearchMenu,
            L('Search'),
            L('SearchPrompt'),
            thumb = R(ICON_SEARCH))))
    
    return dir

####################################################################################################
# VIDCASTS
####################################################################################################

def VidCastMenu(sender, url = VIDCASTS_URL):
    dir = MediaContainer(disabledViewModes=["Coverflow"], title1 = L('Title'), title2 = L('VidCasts')) 

    vidcasts_page = HTML.ElementFromURL(url)
    vidcasts_initial_node = vidcasts_page.xpath("//div[@class='inner-container']/div/h2[contains(text(), 'Vidcasts')]/..")[0]
    vidcasts = vidcasts_initial_node.xpath(".//div[@class='item-list']/ul/li[@class='product']")
    
    for item in vidcasts:
        
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
        next_url = BASE_URL + next_relative_url
        dir.Append(Function(DirectoryItem(
            VidCastMenu,
            L('Next')),
            url = next_url))

    except: 
        pass

    return dir

####################################################################################################
# VIDEO REVIEWS
####################################################################################################

def VideoReviewMenu(sender, url = VIDEO_REVIEWS_URL):
    dir = MediaContainer(disabledViewModes=["Coverflow"], title1 = L('Title'), title2 = L('VideoReviews')) 

    video_reviews_page = HTML.ElementFromURL(url)
    video_reviews_initial_node = video_reviews_page.xpath("//div[@class='inner-container']/div/h2[contains(text(), 'Video reviews')]/..")[0]
    video_reviews = video_reviews_initial_node.xpath(".//div[@class='item-list']/ul/li[@class='product']")

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
        next_relative_url = video_reviews_page.xpath("//div[@class='pagination']/span[@class='next']/a[@class='active']")[0].get('href')
        next_url = BASE_URL + next_relative_url

        dir.Append(Function(DirectoryItem(
            VideoReviewMenu,
            L('Next')),
            url = next_url))

    except: 
        pass

    return dir

####################################################################################################
# Search
####################################################################################################

def SearchMenu(sender, query, url = None):
    dir = MediaContainer(disabledViewModes=["Coverflow"], title1 = L('Title'), title2 = query) 
    
    # If an actual URL has not been specified, we should simply construct one using the search query.
    if url == None:
        url = SEARCH_URL % String.Quote(query)
    
    search_page = HTML.ElementFromURL(url)
    search_page_initial_node = search_page.xpath("//div[@class='inner-container']/h2[contains(text(), 'Stuff Video')]/..")[0]
    search_results = search_page_initial_node.xpath(".//li[contains(concat(' ', normalize-space(@class), ' '), ' product')]")
    
    for item in search_results:
        
        try:
            
            # Attempt to determine the title
            title = item.xpath(".//h3/a/text()")[0]
            
            # Attempt to determine the absolue URL to the page
            relative_url = item.xpath(".//h3/a")[0].get('href')
            url = BASE_URL + String.Quote(relative_url)
            
            # [Optional] - Attempt to determine the subtitle
            subtitle = None
            try: subtitle = item.xpath(".//p[@class='meta']/span/text()")[0]
            except: pass
            
            # [Optional] - Attempt to determine the additional information
            info = None
            try: subtitle = info.xpath(".//p[@class='meta']/text()")[0]
            except: pass
            
            # [Optional] - Attempt to determine the thumbnail
            thumb = None
            try: thumb = item.xpath(".//a/img")[0].get('src')
            except: pass
            
            dir.Append(WebVideoItem(
                url,
                title = title,
                subtitle = subtitle,
                infoLabel = info,
                thumb = thumb))
                
        except: pass
    
    try:
        
        # Attempt to determine if there is more videos available on the next page.
        next_relative_url = search_page.xpath("//div[@class='pagination']/span[@class='next']/a[@class='active']")[0].get('href')
        next_url = BASE_URL + next_relative_url
        dir.Append(Function(DirectoryItem(
            SearchMenu,
            L('Next')),
            query = query,
            url = next_url))
    
    except: 
        pass
    
    # Check to see if we have found any associated videos.
    if len(dir) == 0:
        return MessageContainer("No videos were found")
    
    return dir