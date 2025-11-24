from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.product_add, name='product_add'),
    path('edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('<int:pk>/', views.product_detail, name='product_detail'),  # page détail
    path('dashboard/', views.dashboard, name='dashboard'),
    path("category/<int:category_id>/", views.products_by_category, name="products_by_category"),

    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    path('find-us/', views.find_us, name='find_us'),
    path('add-review/', views.add_review, name='add_review'),
    path('avis/', views.add_review, name='Avis'),
    path('service/', views.service, name='service'),
    path('menu/', views.menu, name='menu'),
    path('reservation/', views.reservation, name='reservation'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('contact/', views.contact, name='contact'),
    
    path("reserve/", views.reserve_table, name="reserve_table"),

]
