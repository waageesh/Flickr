from .models import *
from .views import *
from django.urls import path, re_path, include

# import router modules
from rest_framework.routers import SimpleRouter , DefaultRouter

# group_view = GroupViewSet.as_view({
# 		"get":"list"
# 		# "post":"create"
# 	})

# photo_view = PhotoViewSet.as_view({
# 		"get":"list"
# 		# "post":"cr# 	})


router = DefaultRouter()

router.register('', GroupViewSet, basename = 'group_info_list')
router.register('photos', PhotoViewSet,basename = 'photo_info_list')
router.register(r'groups/(?P<GID>[0-9]{7,11}\@[A-Z][0-9]{2,2})', GroupViewSet,basename = 'group_count_list')
# router.register(r'photos/(?P<GID>[0-9]{7,11}\@[A-Z][0-9]{2,2})', PhotoViewSet,basename = 'photos_count_list')
router.register(r'photos/(?P<ID>[0-9]{7,11})', PhotoViewSet, basename = 'image_display')
# router.register('groups/(?P<GID>[0-9]{7,7}\@[A-Z][0-9]{2,2})', GroupViewSet,basename = 'group_list')
# router.register('photos', PhotoViewSet,basename = 'photos_list')
# router.register('photos', GroupViewSet)




urlpatterns = [
	path('api/v1/',include(router.urls)),
    # path('api/v1/login/', LoginView.as_view(), name='login'),
    # path('api/v1/groups/', GroupsView.as_view(), name='group_info_photos_count'),
    # re_path(r'^api/v1/groups/(?P<GID>[0-9]{7,7}\@[A-Z][0-9]{2,2})/$', GroupPhotoIdView.as_view(), name='group_photos_info'),
    # # /api/v1/photos/?group=<GID>
    # re_path(r'^api/v1/photos/$', GroupPhotosView.as_view(), name='group_photos_display'),
    # re_path(r'^api/v1/photos/(?P<ID>[0-9]{11,11})/$', PhotosDetailsView.as_view(), name='photo_details_info'),
    # path('api/v1/logout/', LogoutView.as_view(), name='logut'),
    # path('index/',HomepageView.as_view(), name='homepage'),
    # path('index/',RegisterView.as_view()),
    # path('index/',HomepageView.as_view()),
]
