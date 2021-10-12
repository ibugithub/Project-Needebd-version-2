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
    path('vchrviewurl/', views.VoucherView, name = 'vchrurlname'),
    # Account realted ...
    path('maccounturl/', views.ManageAccountView.as_view(), name = "maccounturlname"),
    path('profileurl/', views.ProfileView.as_view(), name = "profileurlname"), 
    path('eprofileurl/', views.EditProfileView.as_view(), name = "eprofileurlname"),
    path('abookurl/', views.AddressBookView.as_view(), name = 'abookurlname'), 
    path('aaddressurl/', views.AddAddressView.as_view(), name ='aaddressurlname'),
    path('orderurl/', views.OrderView.as_view(), name="orderurlname"),
    path('cancellationurl/', views.CancellationView.as_view(), name = "cancellationurlname"),
    path('divsetterurl/', views.DivisionSetter),
    path("disfilterurl/", views.DistrictsFilter),
    path("dissetterurl/", views.DistrictSetter),
    path('upafilterurl/', views.UpazilaFilter),
    path('upasetterurl/', views.UpazilaNameSetter),
    path('upaidgiverurl/', views.UpazilaIdGiver),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
