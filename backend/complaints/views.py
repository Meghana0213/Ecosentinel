from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Complaint

from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.conf import settings

import tensorflow as tf
import numpy as np

from PIL import Image, ImageOps


# LOAD AI MODEL

model = tf.keras.models.load_model(
    "ai_model/keras_model.h5",
    compile=False
)

class_names = open(
    "ai_model/labels.txt",
    "r"
).readlines()


# AI WASTE DETECTION

def predict_waste(image_path):

    data = np.ndarray(
        shape=(1, 224, 224, 3),
        dtype=np.float32
    )

    image = Image.open(image_path).convert("RGB")

    size = (224, 224)

    image = ImageOps.fit(
        image,
        size,
        Image.Resampling.LANCZOS
    )

    image_array = np.asarray(image)

    normalized_image_array = (
        image_array.astype(np.float32) / 127.5
    ) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)

    index = np.argmax(prediction)

    class_name = class_names[index]

    return class_name.strip().replace(
        "0 ", ""
    ).replace(
        "1 ", ""
    ).replace(
        "2 ", ""
    ).replace(
        "3 ", ""
    ).replace(
        "4 ", ""
    )


# PRIORITY DETECTION

def detect_priority(description):

    if not description:
        return "Low"

    description = description.lower()

    high_keywords = [
        "hospital",
        "school",
        "danger",
        "urgent",
        "huge",
        "medical"
    ]

    for word in high_keywords:

        if word in description:
            return "High"

    if len(description) > 100:
        return "Medium"

    return "Low"


# HOME PAGE

def home(request):

    if request.method == "POST":

        image = request.FILES.get("image")

        description = request.POST.get(
            "description",
            ""
        )

        detected_waste = "General Waste"

        if image:

            temp_path = "media/temp.jpg"

            with open(
                temp_path,
                "wb+"
            ) as destination:

                for chunk in image.chunks():

                    destination.write(chunk)

            try:

                detected_waste = predict_waste(
                    temp_path
                )

            except Exception as e:

                print(e)

                detected_waste = "General Waste"

        priority = detect_priority(
            description
        )

        # SAVE COMPLAINT

        Complaint.objects.create(

            waste_type=detected_waste,

            location=request.POST.get(
                "location"
            ),

            description=description,

            image=image,

            status=request.POST.get(
                "status",
                "Pending"
            ),

            priority=priority

        )

        # SEND EMAIL

        send_mail(

            'New Waste Complaint Submitted',

            f'''
Waste Type: {detected_waste}

Location:
{request.POST.get("location")}

Priority:
{priority}

Status:
{request.POST.get("status")}
''',

            settings.EMAIL_HOST_USER,

            ['bsmegha13@gmail.com'],

            fail_silently=False

        )

        return redirect("/")

    # FETCH COMPLAINTS

    complaints = Complaint.objects.all().order_by(
        "-created_at"
    )

    search_query = request.GET.get(
        "search"
    )

    if search_query:

        complaints = complaints.filter(
            waste_type__icontains=search_query
        )

    # DASHBOARD COUNTS

    total_complaints = Complaint.objects.count()

    pending_count = Complaint.objects.filter(
        status='Pending'
    ).count()

    completed_count = Complaint.objects.filter(
        status='Resolved'
    ).count()

    # CONTEXT

    context = {

        "complaints": complaints,

        "total_complaints": total_complaints,

        "pending_count": pending_count,

        "completed_count": completed_count,

    }

    return render(
        request,
        "frontend/index.html",
        context
    )


# PDF EXPORT

def export_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="complaints.pdf"'

    p = canvas.Canvas(response)

    complaints = Complaint.objects.all()

    y = 800

    p.setFont(
        "Helvetica-Bold",
        18
    )

    p.drawString(
        180,
        y,
        "AI Smart Waste Monitoring Report"
    )

    y -= 50

    p.setFont(
        "Helvetica",
        12
    )

    for complaint in complaints:

        p.drawString(
            50,
            y,
            f"Waste Type: {complaint.waste_type}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Location: {complaint.location}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Priority: {complaint.priority}"
        )

        y -= 20

        p.drawString(
            50,
            y,
            f"Status: {complaint.status}"
        )

        y -= 40

        if y < 100:

            p.showPage()

            y = 800

    p.save()

    return response
from django.shortcuts import get_object_or_404


def delete_complaint(request, id):

    complaint = get_object_or_404(
        Complaint,
        id=id
    )

    complaint.delete()

    return redirect('/')