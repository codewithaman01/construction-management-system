from django.urls import path
from . import views

urlpatterns = [

    # Pages
    path('', views.store_dashboard),
    path('stock/', views.stock_page),
    path('inward/', views.inward_page),
    path('outward/', views.outward_page),
    path('requirements/', views.requirements_page),

    # Material APIs
    path('get-materials/', views.get_materials),
    path('add-material/', views.add_material),
    path('update-material/', views.update_material),  # ✅ THIS
    path('delete-material/', views.delete_material),

    # Inward
    path('get-inwards/', views.get_inwards),
    path('add-inward/', views.add_inward),

    # Outward
    path('get-outwards/', views.get_outwards),
    path('add-outward/', views.add_outward),

    # Requirement
    path('get-requirements/', views.get_requirements),
    path('add-requirement/', views.add_requirement),
    path('update-requirement/', views.update_requirement),

    # Stats
    path('stats/', views.store_stats),
]