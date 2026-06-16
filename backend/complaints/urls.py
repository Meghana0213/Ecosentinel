from django.urls import path
from .views import home, delete_complaint, export_pdf

urlpatterns = [

    path(
        '',
        home,
        name='home'
    ),

    path(
        'export-pdf/',
        export_pdf,
        name='export_pdf'
    ),

    path(
        'delete/<int:id>/',
        delete_complaint,
        name='delete_complaint'
    ),

]