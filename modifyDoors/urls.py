"""
URL configuration for modifyDoors project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from orders.views import OrdersAPIView, ModifyOrdersAPIView, CheckOrderView, GetModifyView, ModifyDoorsWRListView
from services.views import ServicesAPIView, CharacteristicsAPIView, GetServicesAPIView, GetCharacteristicsAPIView, \
    ServicesUpdate

router = routers.SimpleRouter()
router.register(r'orders', OrdersAPIView)
router.register(r'modify', ModifyOrdersAPIView)
router.register(r'services', ServicesAPIView)
router.register(r'characteristics', CharacteristicsAPIView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/check-order/', CheckOrderView.as_view(), name='check-order'),
    path('api/v1/get-modify/', GetModifyView.as_view(), name='get-modify'),
    path('api/v1/get-services/', GetServicesAPIView.as_view({'get': 'list'}), name='get-services'),
    path('api/v1/', include(router.urls)),
    path('api/v1/get-characteristics/', GetCharacteristicsAPIView.as_view({'get': 'list'}), name='get-characteristics'),
    path('api/v1/put-services/', ServicesUpdate.as_view(), name='put-services'),
    path('api/v1/get-modification/', ModifyDoorsWRListView.as_view(), name='get-modify'),
]
