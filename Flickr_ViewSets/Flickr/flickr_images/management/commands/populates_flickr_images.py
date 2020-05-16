from flickr_images.models import *
import requests

# improt Basecommand to make it as runtime command using "Python manage.py command_name"
from django.core.management.base import BaseCommand

#import flickr api related modules
from flickrapi import FlickrAPI

# import NamedTemporaryFile module and File
from tempfile import NamedTemporaryFile
from django.core.files import File


FLICKR_PUBLIC = '29289b639133aa68cadc36eb27677b17'
FLICKR_SECRET = '00aa9e850946a96b'

flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')


class Command(BaseCommand):

	help = "reading images details from JSON response and forming image URL's"

	# image_urls = []
	# image_records = []
	def add_arguments(self,parser):
		#positional arguments
		parser.add_argument(
			# used as label for using user_input in this code using options["lable_name"]
			# ex: url = options['images_load_from_API_call(url)']
			'images_load_from_url', 
			type=str,
			help="loads images from Flickr API call and populates then into database")
		# optional argument for deleting existing records in model
		# Named (optional) arguments

		parser.add_argument(
    		'--delete-existing',
    		action='store_true',
    		dest='delete_existing',
    		default=False,
    		help='Delete existing images before loading new ones'
    		)


	def photo_url(self, grp_id):
		# url for JSON response of particular group pics
		url = "https://www.flickr.com/services/rest/?method=flickr.groups.pools.getPhotos&api_key=29289b639133aa68cadc36eb27677b17&group_id=2679710%40N21&format=json&nojsoncallback=1"

		# photos details from JSON response of flickr "flickr.groups.pools.getPhotos" API
		# collecting photos details
		photo_json = flickr.groups.pools.getPhotos(api_key=FLICKR_PUBLIC ,group_id=grp_id,per_page=30)
		photos     = photo_json['photos']
		photo_id = []
		photo_secret = []
		photo_server = []
		photo_farm = []
		photo_url = []
		for i in range(len(photos['photo'])):
			photo_id.append(photos['photo'][i]['id'])
			photo_secret.append(photos['photo'][i]['secret'])
			photo_server.append(photos['photo'][i]['server'])
			photo_farm.append(photos['photo'][i]['farm'])
			#creating image url from above image details
			photo_url.append("https://farm"+str(photo_farm[i])+".staticflickr.com/"+str(photo_server[i])+"/"+str(photo_id[i])+"_"+str(photo_secret[i])+".jpg")
		
		#print(photo_id, photo_secret, photo_server, photo_farm, photo_url)
		return(photo_id, photo_secret, photo_server, photo_farm, photo_url)


	# def save_image_from_url(model, url):
	#     r = requests.get(url)

	#     img_temp = NamedTemporaryFile(delete=True)
	#     img_temp.write(r.content)
	#     img_temp.flush()

	#     model.image.save("image.jpg", File(img_temp), save=True)


	def handle(self,*args, **options):

		# as added  in add_arguments method, under parser.add_arguments,
		# we can pass group url as argument from command prompt/shell
		group_url = options['images_load_from_url']

		#  group details from JSON response of flickr "flickr.urls.lookupGroup" API
		#  collecting group details, only after which we can photos details
		group_json = flickr.urls.lookupGroup(api_key=FLICKR_PUBLIC , url = group_url)
		grp = group_json['group']
		grp_id   = grp['id']
		grp_name = grp['groupname']['_content']
		print(grp_id, grp_name)

		photo_id, photo_secret, photo_server, photo_farm, photo_url = self.photo_url(grp_id)

		image_record = []

		#create temp file to store image content
		

		for i in range(len(photo_id)):
			#getting ith image url from photo_url list

			''' 
				saves images from web url/remote to image field in model
			'''
			img_temp = NamedTemporaryFile(delete=True)
			image_req = requests.get(photo_url[i])
			img_temp.write(image_req.content)
			#img_temp.flush()
		    #UploadImages.image.save("image.jpg", File(img_temp), save=True)
		    #UploadImages.image.save('.jpg',ContentFile(img_temp.decode('base-64')),save=False,)

			group_details = {#'image':img_temp,
	                         'group_id':grp_id,
	                         'group_name':grp_name,
	                         'image_id':photo_id[i],
	                         'user':'yavana.vaageesh', # hardcode, as it was mentioned in assignment, to create single user
			                }
			image_model_obj = UploadImages(**group_details)
			image_model_obj.image.save(str(photo_id[i])+".jpg", File(img_temp), save=False)
			# image_mode
			# image_model_obj.image.save('.jpg',ContentFile(img_temp.decode('base-64')),save=False,)
			#adding single image record to a list
			image_record.append(image_model_obj)

			# image_record.append(UploadImages(**group_details))
		
		if options['delete_existing']:
			UploadImages.objects.all().delete()
			self.stdout.write(self.style.SUCCESS('image records deleted sucessfull'))
		# pushing all records into the model
		UploadImages.objects.bulk_create(image_record)

		self.stdout.write(self.style.SUCCESS('images populated sucessfull to the Database'))