from django.urls import path, include
from .views import (AddPropertyView, UpdateProperty,
                    DeletePropertyView, GetAllPropertyView, GetPropertyById, GetPropertyByLocation, GetPropertyByTitle)

urlpatterns = [
    path('add/', AddPropertyView.as_view(), name='add_property'),
    path('all/', GetAllPropertyView.as_view(), name='get_all_property'),
    path('all/<int:id>/', GetPropertyById.as_view(), name='get_property_by_id'),
    path('all/<str:location>/location', GetPropertyByLocation.as_view(),
         name='get_property_by_location'),
    path('all/<str:title>/title', GetPropertyByTitle.as_view(),
         name='get_property_by_title'),
    path('update/<int:id>', UpdateProperty.as_view(), name='update_property'),
    path('delete/<int:id>', DeletePropertyView.as_view(), name='delete_property'),
]
