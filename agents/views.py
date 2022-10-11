import random
import math
from urllib import request
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import Is_OrganiserAndLoginRequiredMixin

# Create your views here.
class AgentListView(Is_OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = "agent_list.html"
    queryset = Agent.objects.all().order_by("-id")
    context_object_name = "agents"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation).order_by("-id")

class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent_list")

    def password(self, num):
        digits = "0123456789"
        OTP = ""

        for i in range(6):
            OTP += digits[math.floor(random.random()*num)]

        return OTP


    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        password = self.password(10)
        user.set_password(password)
        user.save()
        Agent.objects.create(
            user= user, 
            organisation= self.request.user.userprofile )
        send_mail(
            subject="You have been invited as an Agent",
            message="You have been added as an agent on Lantern Cafe CRM. Please come login to start working on your new leads. Email - "+ user.email +", Password - " + password,
            from_email = "test@test.com",
            recipient_list= [user.email]
        )

        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(Is_OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = "agent_details.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentUpdateView(Is_OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent_list")

    def get_queryset(self):
        user = self.request.user
        organisation = user.userprofile
        queryset = Agent.objects.filter(organisation=organisation)
        return queryset

class AgentDeleteView(Is_OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agent_delete.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse("agents:agent_list")