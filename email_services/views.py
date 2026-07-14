from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from .models import EmailCampaign

def campaigns(request):
    if request.method == 'POST':
        data = request.POST
        subject = data.get('subject')
        body = data.get('body')
        attachment = request.FILES.get('attachment')

        if not subject or not body:
            messages.error(request, "Subject and Body are required fields.")
            return redirect('/')

        EmailCampaign.objects.create(
            subject=subject,
            body=body,
            attachment=attachment
        )
        messages.success(request, f"Email campaign template '{subject}' created successfully!")
        return redirect('/')

    queryset = EmailCampaign.objects.all().order_by('-created_at')
    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(subject__icontains=search_query)

    context = {
        'campaigns': queryset,
        'search_query': search_query or ''
    }
    return render(request, 'dashboard.html', context)


def delete_campaign(request, id):
    campaign = get_object_or_404(EmailCampaign, id=id)
    subject = campaign.subject
    campaign.delete()
    messages.success(request, f"Campaign '{subject}' deleted successfully.")
    return redirect('/')


def update_campaign(request, id):
    campaign = get_object_or_404(EmailCampaign, id=id)
    if request.method == 'POST':
        data = request.POST
        subject = data.get('subject')
        body = data.get('body')
        attachment = request.FILES.get('attachment')

        if not subject or not body:
            messages.error(request, "Subject and Body cannot be empty.")
            return redirect(f'/update_campaign/{id}')

        campaign.subject = subject
        campaign.body = body
        if attachment:
            campaign.attachment = attachment
        campaign.save()

        messages.success(request, f"Campaign '{subject}' updated successfully!")
        return redirect('/')

    context = {'campaign': campaign}
    return render(request, 'update_campaign.html', context)


def send_test_email(request, id):
    if request.method == 'POST':
        campaign = get_object_or_404(EmailCampaign, id=id)
        recipient = request.POST.get('recipient_email')
        
        if not recipient:
            messages.error(request, "Recipient email is required to send.")
            return redirect('/')

        try:
            # We configure Django mail to print to console backend in settings.py
            send_mail(
                subject=campaign.subject,
                message=campaign.body,
                from_email='noreply@aeromail.local',
                recipient_list=[recipient],
                fail_silently=False,
            )
            
            # Increment sent count
            campaign.sent_count += 1
            campaign.save()
            
            messages.success(request, f"Test email for '{campaign.subject}' successfully queued/sent to {recipient}!")
        except Exception as e:
            messages.error(request, f"Failed to send email: {str(e)}")
            
    return redirect('/')
