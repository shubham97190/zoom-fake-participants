from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from _thread import start_new_thread

from zoom_client.utility import add_participants, remove_meeting

# Create your views here.


class HomeView(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        meeting_code = request.POST.get('meeting_code')
        meeting_password = request.POST.get('meeting_password')
        no_of_participants = request.POST.get('no_of_participants')
        context = {
            'meeting_code': meeting_code,
            'meeting_password': meeting_password,
            'no_of_participants': no_of_participants
        }
        start_new_thread(add_participants,(meeting_code, meeting_password, no_of_participants))
        return render(request, self.template_name, context=context)


class MeetingView(View):

    def post(self, request, *args, **kwargs):
        meeting_code = request.POST.get('id')
        start_new_thread(remove_meeting,(meeting_code,))
        return HttpResponse(request)
    