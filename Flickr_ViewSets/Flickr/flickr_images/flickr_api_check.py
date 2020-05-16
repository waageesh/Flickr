from flickrapi import FlickrAPI

FLICKR_PUBLIC = '29289b639133aa68cadc36eb27677b17'
FLICKR_SECRET = '00aa9e850946a96b'

flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
#extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
group_urls = ['https://www.flickr.com/groups/flickrheroes/']

#collecting group details, only after we can photos details
group_json = flickr.urls.lookupGroup(api_key=FLICKR_PUBLIC , url = group_urls[0])
grp = group_json['group']
grp_id   = grp['id']
grp_name = grp['groupname']['_content']
print(grp_id, grp_name)

# collecting photos details
photo_json = flickr.groups.pools.getPhotos(api_key=FLICKR_PUBLIC ,group_id=grp_id,per_page=30)
photos       = photo_json['photos']
print(len(photos['photo']))
photo_id     = photos['photo'][0]['id']
photo_secret = photos['photo'][0]['secret']
photo_server = photos['photo'][0]['server']
photo_farm   = photos['photo'][0]['farm']

#print(photo_id, photo_secret, photo_server, photo_farm)
image_url = "https://farm"+str(photo_farm)+".staticflickr.com/"+str(photo_server)+"/"+str(photo_id)+"_"+str(photo_secret)+".jpg"
print(image_url)
# cats = flickr.photos.search(text='kitten', per_page=5, extras=extras)
# photos = cats['photos']
# from pprint import pprint
# pprint(photos)