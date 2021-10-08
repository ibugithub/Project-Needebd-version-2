from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('account/', views.account, name='account'),
    path('allcategoryurl/',views.AllCategoryView.as_view(), name='allcategory-url-name'),
    path('productpageurl/<category>/',views.ProductPageView.as_view(), name= 'productpageurlname'),
    path('singleproducturl/<int:pk>/', views.SingleProductView.as_view(), name= 'singleproducturlname'),
    path('addtocarturl/', views.AddToCartView, name= 'addtocarturlname'),
    path('showcarturl/',views.ShowCartView.as_view(), name= 'showcarturlname'),
    path('pluscarturl/', views.PlusCartView, name = 'pluscarturlname'),
    path('minuscarturl/', views.MinusCartView, name= 'minuscarturlname'),
    path('removecarturl/', views.RemoveCartView, name = 'removecarturlname'),
    path('vcurl/', views.VoucherChecker, name = "vcurlname"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
