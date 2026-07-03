import qrcode
import base64
from io import BytesIO

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from .forms import RegistrationForm
from .models import Registration
from events.models import Event

from django.http import JsonResponse

from django.db.models import Sum
from django.shortcuts import render
from .models import Registration


def dashboard(request):
    registrations = Registration.objects.all().order_by('-created_at')

    total_registrations = registrations.count()
    total_revenue = registrations.aggregate(
        total=Sum('registration_fee')
    )['total'] or 0

    total_pledges = registrations.aggregate(
        total=Sum('pledge')
    )['total'] or 0

    context = {
        "registrations": registrations,
        "total_registrations": total_registrations,
        "total_revenue": total_revenue,
        "total_pledges": total_pledges,
    }

    return render(request, "registrations/dashboard.html", context)

def register(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.save()

            return render(request, 'registrations/success.html', {
                'registration': registration
            })
    else:
        form = RegistrationForm()

    return render(request, 'registrations/register.html', {
        'form': form,
        'event': event,
    })
    def verify_registration(request, reg_number):
     registration = get_object_or_404(Registration, registration_number=reg_number)

    return render(request, "registrations/verify.html", {
        "registration": registration
    })

def verify_registration(request, reg_number):
    try:
        registration = Registration.objects.get(registration_number=reg_number)

        return render(request, "registrations/verify.html", {
            "registration": registration,
            "status": "VALID"
        })

    except Registration.DoesNotExist:
        return render(request, "registrations/verify.html", {
            "status": "INVALID"
        })
    

# ✅ PDF DOWNLOAD VIEW
def download_receipt_pdf(request, pk):
    registration = get_object_or_404(Registration, id=pk)

    # 🔥 QR CODE CONTENT (verification link)
    verify_url = request.build_absolute_uri(
        f"/registrations/verify/{registration.registration_number}/"
    )

    qr = qrcode.make(verify_url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    context = {
        "registration": registration,
        "qr_code": qr_base64
    }

    html = render_to_string("registrations/success.html", context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{registration.registration_number}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response