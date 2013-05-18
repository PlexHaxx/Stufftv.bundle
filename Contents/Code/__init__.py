NAME = L('Title')
BASE_URL = "http://www.stuff.tv"
VIDCASTS_URL = "http://www.stuff.tv/video/vidcasts"
VIDEO_REVIEWS_URL = "http://www.stuff.tv/video/reviews"

####################################################################################################
def Start():

	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
	ObjectContainer.title1 = NAME
	ObjectContainer.view_group = 'List'
	HTTP.CacheTime = CACHE_1DAY

####################################################################################################
@handler('/video/stufftv', NAME)
def MainMenu():

	oc = ObjectContainer()

	oc.add(DirectoryObject(key = Callback(VidCastMenu), title=L('VidCasts')))
	oc.add(DirectoryObject(key = Callback(VideoReviewMenu), title=L('VideoReviews')))
	oc.add(SearchDirectoryObject(identifier="com.plexapp.plugins.stufftv", title=L('Search'), prompt=L('SearchPrompt')))

	return oc

####################################################################################################
# VIDCASTS
####################################################################################################
@route('/video/stufftv/videocasts', allow_sync=True)
def VidCastMenu(url = VIDCASTS_URL):

	oc = ObjectContainer(title2=L('VidCasts'))

	vidcasts_page = HTML.ElementFromURL(url)
	vidcasts_initial_node = vidcasts_page.xpath("//div[@class='inner-container']/div/h2[contains(text(), 'Vidcasts')]/..")[0]
	vidcasts = vidcasts_initial_node.xpath(".//div[@class='item-list']/ul/li//div[contains(@class, 'product')]")

	for item in vidcasts:
		 try:
			 # Attempt to determine the title
			 title = item.xpath(".//h4/a/text()")[0]

			 # Attempt to determine the absolue URL to the page
			 relative_url = item.xpath(".//div/a/@href")[0]
			 url = '%s%s' % (BASE_URL, relative_url)

			 # [Optional] - Attempt to determine the date
			 try:
				 date = item.xpath(".//p[@class='meta']/text()")[0]
				 date = Datetime.ParseDate(date)
			 except: date = None

			 # [Optional] - Attempt to determine the thumbnail
			 try:
				 thumb_url = item.xpath(".//div/a/img/@src")[0]
				 thumb = thumb_url.replace('/imagecache/video_thumb/', '/').replace('/imagecache/review_thumb/', '/')
			 except: thumb = ''

			 oc.add(VideoClipObject(
				 url = url,
				 title = title,
				 thumb = Resource.ContentsOfURLWithFallback(thumb),
				 originally_available_at = date
			 ))

		 except:
			 pass

	try:
		# Attempt to determine if there is more videos available on the next page.
		next_relative_url = vidcasts_page.xpath("//div[@class='pagination']/span[@class='next']/a[@class='active']/@href")[0]
		next_url = '%s%s' % (BASE_URL, next_relative_url)

		oc.add(NextPageObject(
			key = Callback(VidCastMenu, url=next_url),
			title = L('Next')
		))

	except:
		pass

	return oc

####################################################################################################
# VIDEO REVIEWS
####################################################################################################
@route('/video/stufftv/reviews', allow_sync=True)
def VideoReviewMenu(url = VIDEO_REVIEWS_URL):

	oc = ObjectContainer(title2=L('VideoReviews'))

	video_reviews_page = HTML.ElementFromURL(url)
	video_reviews_initial_node = video_reviews_page.xpath("//div[@class='inner-container']/div/h2[contains(text(), 'Video reviews')]/..")[0]
	video_reviews = video_reviews_initial_node.xpath(".//div[@class='item-list']/ul/li//div[contains(@class,'product')]")

	for item in video_reviews:
		 try:
			 # Attempt to determine the title
			 title = item.xpath(".//h4/a/text()")[0]

			 # Attempt to determine the absolue URL to the page
			 relative_url = item.xpath(".//div/a/@href")[0]
			 url = '%s%s' % (BASE_URL, relative_url)

			 # [Optional] - Attempt to determine the subtitle
			 try:
				 date = item.xpath(".//p[@class='meta']/text()")[0]
				 date = Datetime.ParseDate(date)
			 except: date = None

			 # [Optional] - Attempt to determine the thumbnail
			 try:
				 thumb_url = item.xpath(".//div/a/img/@src")[0]
				 thumb = thumb_url.replace('/imagecache/video_thumb/', '/').replace('/imagecache/review_thumb/', '/')
			 except: thumb = ''

			 oc.add(VideoClipObject(
				 url = url,
				 title = title,
				 thumb = Resource.ContentsOfURLWithFallback(thumb),
				 originally_available_at = date
			 ))

		 except:
			 pass

	try:
		# Attempt to determine if there is more videos available on the next page.
		next_relative_url = video_reviews_page.xpath("//div[@class='pagination']/span[@class='next']/a[@class='active']/@href")[0]
		next_url = '%s%s' % (BASE_URL, next_relative_url)

		oc.add(NextPageObject(
			key = Callback(VideoReviewMenu, url=next_url),
			title = L('Next')
		))

	except:
		pass

	return oc
