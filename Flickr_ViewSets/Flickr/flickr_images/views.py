from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
#import Django paginator
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage

# Create your views here.

from django.db.models import Avg , Max, Count, Sum
from rest_framework import viewsets
from rest_framework.decorators import action
'''
viewset for group details
'''
class GroupViewSet(viewsets.ModelViewSet):
	serializer_class = GroupSerializer
	# queryset = UploadImages.objects.all()

	def get_queryset(self): ##api/v1/groups/2679710@N21
		try:
			if not self.kwargs['GID']:
				queryset = UploadImages.objects.all()
				return queryset
			id = self.kwargs['GID']
			queryset = UploadImages.objects.filter(group_id=id)
			# queryset = queryset.annotate(img_cnt=Count('group_id'))
			# img_id = []
			# for obj in queryset:
			# 	id = obj.image_id
			# 	img_id.append(id)
			# return queryset.values()
			return queryset
		except KeyError:
			queryset = UploadImages.objects.all()
	


	@action(detail=False, methods=["GET"])
	def groups(self, request, GID=None):

		'''
		below is code for 2 API's
		--> api/v1/groups
		--> api/v1/groups/?group=<GID>
		'''
		
		query_GID = self.request.query_params.get('group')
		grp_id = []
		img_cnt = []
		if not query_GID:  #api/v1/groups
			for group in UploadImages.objects.values('group_id').distinct():
				grp_id.append(group['group_id'])
			for id in grp_id:
				img_cnt.append(UploadImages.objects.filter(group_id=id).count())
			return Response([grp_id,img_cnt])
		elif query_GID:        #api/v1/groups/?group=<GID>
			images = UploadImages.objects.filter(group_id=query_GID).values('image')
			return Response([query_GID, images  ])
		else:
			qs = self.queryset
			img_id = []
			for obj in qs:
				id = obj.image_id
				img_id.append(id)
			return img_id

class PhotoViewSet(viewsets.ModelViewSet):
	# import ipdb;ipdb.set_trace()
	serializer_class = PhotoSerializer
	# queryset = UploadImages.objects.filter(image_id='14379388986')

	def get_queryset(self): ## api/v1/photos/14379388986/
		try:
			id = self.kwargs['ID']
			queryset = UploadImages.objects.filter(image_id=id)
			return queryset
		except:
			queryset = UploadImages.objects.all()
			return queryset	

	'''
	below is the API for getting photo details
	'''
	# @detail_route(methods=['get'], url_path='api/v1/photos', url_name='photo_info_list')
	# def retrieve(request, *args, **kwargs):
	# 	photos = get_object_or_404(queryset, pk=pk)
	# 	query_GID = self.request.query_params.get('group')
	# 	images = UploadImages.objects.filter(group_id=query_GID).values('image')
	# 	serializer = PhotoSerializer(images)
	# 	return Response(serializer.data)	


	@action(detail=False, methods=["GET"])
	def photos(self, request):    ##api/v1/photos/?group=2679710@N21
		query_GID = self.request.query_params.get('group')
		if self.get_object():
			query_GID = self.get_object()
		# grp_id = UploadImages.objects.filter(group_id=query_GID)
		
		# if not grp_id:  #api/v1/groups
		# 	return Response([grp_id,img_cnt])
		if query_GID:        #api/v1/groups/?group=<GID>
			images = UploadImages.objects.filter(group_id=query_GID).values('image')
			# print('hello world')
			return Response(images)
			# return Response('hello world')
		else:
			id = self.kwargs['ID']
			queryset = UploadImages.objects.filter(image_id=id)
			return Response(queryset)




# class HomepageView(APIView):
# 	def get(self,request):
# 		return render(request,'index.html')

# # login API when called with an username and password should return a Token
# class LoginView(APIView): 
# 	pass



#  API when called with the appropriate USER TOKEN using
#  DRF token authentication should return all the groups that below to the user with
#  details such as group name, group id, number of photos etc. 
# class GroupsView(APIView):

# 	def post(self,request):
# 		grp_id = request.POST.get('group_id')
# 		if grp_id:
# 			return redirect(reverse('GroupPhotoIdView',kwargs={'grp_id':grp_id}))

# 	def get(self,request):

# 		groups_info = UploadImages.objects.values('user','group_name','group_id','image_id').annotate(image_cnt=Count('group_name'))

# 		grp_names_unique = UploadImages.objects.values('group_name').distinct()
# 		grp_info = []
# 		for each in grp_names_unique:
# 			grp_name = each['group_name']
# 			grp_pics_cnt = UploadImages.objects.filter(group_name=grp_name).count()
# 			grp_id_qryset = UploadImages.objects.filter(group_name=grp_name).values('group_id').distinct()
# 			grp_id = grp_id_qryset[0]['group_id']
# 			grp_info.append([grp_name,grp_id,grp_pics_cnt])
# 		grp_no = len(grp_info)
# 		'''
# 		paginator for paginate the final group objects 

# 		'''
# 		page = request.GET.get('page',1)
# 		paginator = Paginator(grp_info, 1)

# 		try:
# 			grp_paginated = paginator.page(page)
# 		except PageNotAnInteger:
# 			grp_paginated = paginator.page(1)
# 		except EmptyPage:
# 			grp_paginated = paginator.page(paginator.num_pages)
# 		#return render(request , 'groups_info.html', context={'grp_info':grp_info,'grp_no':range(grp_no)})
# 		return render(request , 'groups_info_paginated.html', context={'grp_paginated':grp_paginated,'grp_no':range(grp_no)})


# #  API when called with the appropriate USER TOKEN using DRF token authentication 
# #  should return all the photos <ID> belonging to the group 
# class GroupPhotoIdView(APIView):
# 	def get(self,request,GID):
# 		# images_ids = []
# 		# for each in UploadImages.objects.filter(group_id = GID).values('image_id'):
# 		# 	images_ids.append([each['image_id'],GID])

# 		'''
# 		paginator for paginate the final list objects 

# 		'''
# 		images_ids = UploadImages.objects.filter(group_id = GID).values('group_id','image_id')
# 		page = request.GET.get('page',1)
# 		paginator = Paginator(images_ids, 10)

# 		try:
# 			images_ids_paginated = paginator.page(page)
# 		except PageNotAnInteger:
# 			images_ids_paginated = paginator.page(1)
# 		except EmptyPage:
# 			images_ids_paginated = paginator.page(paginator.num_pages)

# 		return render(request,'image-id.html',context={'grp_id':GID,'images_ids_paginated':images_ids_paginated})

# #  API when called with the appropriate USER TOKEN using DRF token authentication and 
# #  supplying a group id should return all the photos belonging to the group
# class GroupPhotosView(APIView):
# 	def get(self,request):
# 		GID = str(request.GET.get('group'))
# 		images_obj = UploadImages.objects.filter(group_id = GID)
# 		'''
# 		paginator for paginate the final list objects 

# 		'''
# 		page = request.GET.get('page',1)
# 		paginator = Paginator(images_obj, 10)
# 		try:
# 			images_paginated = paginator.page(page)
# 		except PageNotAnInteger:
# 			images_paginated = paginator.page(1)
# 		except EmptyPage:
# 			images_paginated = paginator.page(paginator.num_pages)

# 		return render(request,'images_display.html',context={'images_paginated':images_paginated})


# #  API when called with photo ID gives details  about that particular photo
# class PhotosDetailsView(APIView):
# 	def get(self,request,ID):
# 		images_obj = UploadImages.objects.filter(image_id = ID)
# 		'''
# 		paginator for paginate the final list objects 

# 		'''
# 		page = request.GET.get('page',1)
# 		paginator = Paginator(images_obj, 10)
# 		try:
# 			image_details_paginated = paginator.page(page)
# 		except PageNotAnInteger:
# 			image_details_paginated = paginator.page(1)
# 		except EmptyPage:
# 			image_details_paginated = paginator.page(paginator.num_pages)

# 		return render(request,'image_details.html',context={'image_details_paginated':image_details_paginated})		

# class LogoutView(APIView):
# 	pass