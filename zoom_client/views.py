from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from zoom_client.models import StoreMetting
from _thread import start_new_thread

from zoom_client.utility import add_participants, remove_meeting

# Create your views here.


class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = {
            "store_objects":StoreMetting.objects.all()
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        meeting_code = request.POST.get('meeting_code')
        meeting_password = request.POST.get('meeting_password')
        no_of_participants = request.POST.get('no_of_participants')
        data = {
            'meeting_code': meeting_code,
            'meeting_password': meeting_password,
            'no_of_participants': no_of_participants
        }
        try:
            obj = StoreMetting.objects.get(meeting_code=meeting_code)
            obj.no_of_participants = obj.no_of_participants+int(no_of_participants)
            obj.save()
        except StoreMetting.DoesNotExist:
            StoreMetting.objects.create(**data)
        start_new_thread(add_participants,(meeting_code, meeting_password, no_of_participants))
        context = {
            "data":data,
            "store_objects":StoreMetting.objects.all()
        }
        print(StoreMetting.objects.all())
        return render(request, self.template_name, context=context)


class MeetingView(View):

    def post(self, request, *args, **kwargs):
        meeting_code = request.POST.get('id')
        start_new_thread(remove_meeting,(meeting_code,))
        StoreMetting.objects.filter(meeting_code=meeting_code).delete()
        return HttpResponse(request)
    