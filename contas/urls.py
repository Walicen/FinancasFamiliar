from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'fatura', api.FaturaViewSet)
router.register(r'conta', api.ContaViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
path('home/', views.Home.as_view(), name='home'),
)


urlpatterns += (
    # urls for Fatura
    path('fatura/', views.FaturaListView.as_view(), name='contas_fatura_list'),
    path('fatura/create/', views.FaturaPagarCreateView.as_view(), name='contas_fatura_create'),
    path('fatura/detail/<int:pk>/', views.FaturaDetailView.as_view(), name='contas_fatura_detail'),
    path('fatura/update/<int:pk>/', views.FaturaUpdateView.as_view(), name='contas_fatura_update'),
)

urlpatterns += (
    # urls for Conta
    path('conta/', views.ContaListView.as_view(), name='contas_conta_list'),
    path('conta/create/', views.ContaCreateView.as_view(), name='contas_conta_create'),
    path('conta/detail/<int:pk>/', views.ContaDetailView.as_view(), name='contas_conta_detail'),
    path('conta/update/<int:pk>/', views.ContaUpdateView.as_view(), name='contas_conta_update'),
)
