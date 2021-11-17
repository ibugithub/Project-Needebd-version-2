from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('account/', views.account, name='account'),
    path('allcategoryurl/',views.AllCategoryView.as_view(), name='allcategory-url-name'),
    path('productpageurl/<category>/',views.ProductPageView.as_view(), name= 'productpageurlname'),
    path('singleproducturl/<int:pk>/', views.SingleProductView, name= 'singleproducturlname'),
    path('addtocarturl/', views.AddToCartView, name= 'addtocarturlname'),
    path('showcarturl/',views.ShowCartView.as_view(), name= 'showcarturlname'),
    path('scheckerurl/',views.stockCheckerView, name = "scheckerurlname"),
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
    path('dfadrmaker/', views.defaultAddressMaker),
    path('aaddressurl/', views.AddAddressView.as_view(), name ='aaddressurlname'),
    url(r'^aaddressurl/(?P<pk>\d+)$', views.AddAddressView.as_view(), name = 'aaddressurlname'),
    path('orderurl/', views.OrderView.as_view(), name="orderurlname"),
    path('cancelorderurl/<int:pk>/', views.CancelOrderView, name='cancelorderurlname' ),
    path('cancellationurl/', views.CancellationView.as_view(), name = "cancellationurlname"),
    path('rorderurl/', views.ReturnedOrderView.as_view(), name = "rorderurlname"),
    path("rmakerurl/<int:pk>/", views.ReturnOrderView, name = "rmakerurlname"),
    path('checkouturl/', views.Checkout, name = "checkouturlname"),
    path('sadrurl/', views.SelectAddressView, name = "sadrurlname"),
    url(r'^buynow/(?P<pk>\d+)$', views.Buynow, name = "buynowurlname"),
    path('buynowurl/',views.Buynow),
    path('buynowdataurl/', views.buyNowDataView, name = 'buynowdataurlname'),
    path('bNVCheckerurl/', views.buyNowVoucherCheckerView, name = "bNVCheckerurlname"),
    path('paymentpageurl/', views.paymentPageView.as_view(), name = 'paymentpageurlname'),
    path('paymentpageurl/<buyNowTunnel>/', views.paymentPageView.as_view(), name = 'paymentpageurlname'),
    path('mmucheckerurl/', views.minMaxUnitCheckerView, name = "mmucheckerurlname"),
    path('bwordermakerurl/', views.buyNowOrderMakerView, name = "bwordermakerurlname"),
    path('ctordermakerurl/',views.cartOrderMakerView, name = 'ctordermakerurlname')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
