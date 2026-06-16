from django.shortcuts import render, redirect
from complaints.models import Complaint

def home(request):

    if request.method == 'POST':

        waste_type = request.POST.get('waste_type')
        location = request.POST.get('location')
        description = request.POST.get('description')
        status = request.POST.get('status')
        image = request.FILES.get('image')

        Complaint.objects.create(
            waste_type=waste_type,
            location=location,
            description=description,
            status=status,
            image=image
        )

        return redirect('/')

    complaints = Complaint.objects.all().order_by('-created_at')

    total_complaints = complaints.count()
    pending_count = complaints.filter(status='Pending').count()
    completed_count = Complaint.objects.filter(
    status='Resolved'
).count()
    context = {
        'complaints': complaints,
        'total_complaints': total_complaints,
        'pending_count': pending_count,
        'completed_count': completed_count,
    }

    return render(request, 'frontend/index.html', context)