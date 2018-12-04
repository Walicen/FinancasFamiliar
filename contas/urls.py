
from django.urls import path, include
from rest_framework import routers

from . import api
from . import views
from allauth.account import views as v
router = routers.DefaultRouter()
router.register(r'fatura', api.FaturaViewSet)
router.register(r'conta', api.ContaViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    path('home', views.Home.as_view(), name='home'),
    path('perfil/<int:pk>/', views.PerfilViewDetail.as_view(), name='perfil'),
    path('', v.login, name="account_login"),
   # path('logout', v.logout,{'next_page': '/'}, name='account_logout')
    path('', views.logout_view , name='logout'),
)

urlpatterns += (
    # urls for Fatura
    path('fatura/', views.FaturaListView.as_view(), name='contas_fatura_list'),
    path('fatura/create/', views.FaturaPagarCreateView.as_view(), name='contas_fatura_create'),
    path('fatura/detail/<int:pk>/', views.FaturaDetailView.as_view(), name='contas_fatura_detail'),
    path('fatura/update/<int:pk>/', views.FaturaUpdateView.as_view(), name='contas_fatura_update'),
    path('fatura/movimentacao/<int:fatura>', views.MovimentacaoView.as_view(), name='movimentacao'),
    path('fatura/projecao', views.ProjecaoView.as_view(), name='projecao')

)

urlpatterns += (
    # urls for Conta
    path('conta/', views.ContaListView.as_view(), name='contas_conta_list'),
    path('conta/create/', views.ContaCreateView.as_view(), name='contas_conta_create'),
    path('conta/detail/<int:pk>/', views.ContaDetailView.as_view(), name='contas_conta_detail'),
    path('conta/update/<int:pk>/', views.ContaUpdateView.as_view(), name='contas_conta_update'),
    path('conta/transferencia', views.TransferenciaView.as_view(), name='transferencia')
)
