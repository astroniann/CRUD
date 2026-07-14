from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from .models import EmailCampaign

class EmailCampaignTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a sample campaign
        self.campaign = EmailCampaign.objects.create(
            subject="Test Subject",
            body="Test body content.",
            sent_count=0
        )

    def test_campaign_creation_and_string_representation(self):
        """Test model creation and __str__ output"""
        self.assertEqual(str(self.campaign), "Test Subject")
        self.assertEqual(self.campaign.sent_count, 0)

    def test_dashboard_view_and_search(self):
        """Test dashboard index view and search query filtering"""
        # Load dashboard page
        response = self.client.get(reverse('campaigns'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Subject")
        
        # Test search matching
        response_search_match = self.client.get(reverse('campaigns'), {'search': 'Test'})
        self.assertContains(response_search_match, "Test Subject")

        # Test search non-matching
        response_search_miss = self.client.get(reverse('campaigns'), {'search': 'UnmatchedQuery'})
        self.assertNotContains(response_search_miss, "Test Subject")

    def test_create_campaign_post(self):
        """Test creation of a campaign template via POST request"""
        # Upload placeholder file
        attachment_file = SimpleUploadedFile("newsletter.txt", b"Newsletter content here", content_type="text/plain")
        
        response = self.client.post(reverse('campaigns'), {
            'subject': 'New Campaign',
            'body': 'Welcome new users!',
            'attachment': attachment_file
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home
        
        # Check database
        new_campaign = EmailCampaign.objects.get(subject='New Campaign')
        self.assertEqual(new_campaign.body, 'Welcome new users!')
        self.assertTrue(new_campaign.attachment.name.endswith('newsletter.txt'))

    def test_update_campaign_post(self):
        """Test updating campaign subject/body fields"""
        response = self.client.post(reverse('update_campaign', args=[self.campaign.id]), {
            'subject': 'Updated Subject',
            'body': 'Updated Body Content'
        })
        self.assertEqual(response.status_code, 302)
        
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.subject, 'Updated Subject')
        self.assertEqual(self.campaign.body, 'Updated Body Content')

    def test_delete_campaign_get(self):
        """Test deleting a campaign from the dashboard"""
        response = self.client.get(reverse('delete_campaign', args=[self.campaign.id]))
        self.assertEqual(response.status_code, 302)
        
        with self.assertRaises(EmailCampaign.DoesNotExist):
            EmailCampaign.objects.get(id=self.campaign.id)

    def test_send_test_email(self):
        """Test sending a mock email (checks sent count and console backend output)"""
        recipient_email = "recipient@example.com"
        
        response = self.client.post(reverse('send_campaign', args=[self.campaign.id]), {
            'recipient_email': recipient_email
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify sent count incremented
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.sent_count, 1)
        
        # Verify Django's outbox contains our email
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        self.assertEqual(sent_mail.subject, self.campaign.subject)
        self.assertEqual(sent_mail.body, self.campaign.body)
        self.assertIn(recipient_email, sent_mail.to)
