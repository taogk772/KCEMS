import qrcode
import base64
from io import BytesIO

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum

from xhtml2pdf import pisa

from django.conf import settings

from .forms import RegistrationForm
from .models import Registration
from events.models import Event


# =========================
# DASHBOARD
# =========================
def dashboard(request):
    registrations = Registration.objects.all().order_by('-created_at')

    total_registrations = registrations.count()

    total_revenue = registrations.aggregate(
        total=Sum('registration_fee')
    )['total'] or 0

    total_pledges = registrations.aggregate(
        total=Sum('pledge')
    )['total'] or 0

    return render(request, "registrations/dashboard.html", {
        "registrations": registrations,
        "total_registrations": total_registrations,
        "total_revenue": total_revenue,
        "total_pledges": total_pledges,
    })


# =========================
# SUCCESS PAGE
# =========================
def registration_success(request, pk):
    registration = get_object_or_404(Registration, id=pk)

    return render(request, "registrations/success.html", {
        "registration": registration
    })


# =========================
# REGISTER VIEW (OPTIMIZED FOR RENDER)
# =========================
def register(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.save()

            full_name = f"{registration.first_name} {registration.last_name}"

            # =========================
            # EMAIL DISABLED (TEMPORARY FOR STABILITY)
            # =========================
            print("EMAIL SKIPPED - Render stable mode")

            # =========================
            # IMPORTANT: SINGLE RETURN ONLY
            # =========================
            return redirect('registration_success', pk=registration.id)

        else:
            print("FORM ERRORS:", form.errors)

    else:
        form = RegistrationForm()

    return render(request, "registrations/register.html", {
        "form": form,
        "event": event,
    })


# =========================
# VERIFY REGISTRATION
# =========================
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


# =========================
# PDF RECEIPT
# =========================
def download_receipt_pdf(request, pk):
    registration = get_object_or_404(Registration, id=pk)

    verify_url = request.build_absolute_uri(
        f"/registrations/verify/{registration.registration_number}/"
    )

    qr = qrcode.make(verify_url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    html = render_to_string("registrations/success.html", {
        "registration": registration,
        "qr_code": qr_base64
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{registration.registration_number}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response