from distutils.log import Log
from urllib import request
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views import generic
from .models import Lead, Agent, Category
from agents.mixins import Is_OrganiserAndLoginRequiredMixin
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, CategoryModelForm

# Create your views here.
# CRUD-L - create, retrive, update and delete + list

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse('login')

class LandingPageView(generic.TemplateView):
    template_name = "landing_page.html"

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # Initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.order_by("-id").filter(
                organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.order_by("-id").filter(
                organisation=user.agent.organisation, agent__isnull=False)
            # filter the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset 

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organizer:
            queryset = Lead.objects.order_by("-id").filter(
                organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset,
            })
        return context
        
class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "lead_details.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.order_by("-id").filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.order_by("-id").filter(organisation=user.agent.organisation)
            # filter the agent that is logged in
            queryset = queryset.filter(agent__user=user)

        return queryset 

class LeadCreateView(Is_OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse('leads:leads')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject = "A lead has been created",
            message = "Go to the site to see the new lead",
            from_email = "test@test.com",
            recipient_list= ["biopythonemail@gmail.com"]       )
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(Is_OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm
    queryset = Lead.objects.all()
    
    def get_success_url(self):
        return reverse('leads:leads')

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organisation=user.userprofile)
        # queryset = queryset.order_by("-id")

        return queryset 

class LeadDeleteView(Is_OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "lead_delete.html"
    queryset = Lead.objects.all()
    
    def get_success_url(self):
        return reverse('leads:leads')

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organisation=user.userprofile)
        # queryset = queryset.order_by("-id")
        
        return queryset 

class AssignAgentView(Is_OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = "assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:leads")

    def form_valid(self, form):
        # print(form.cleaned_data['agent'])
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
                
        context.update({
            "unassigned_leads_count" : queryset.filter(category__isnull=True).count()
        })

        return context 
    
    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.all()
        # Initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Category.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation)
          
        return queryset 

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     leads = self.get_object().leads.all()
                
    #     context.update({
    #         "leads" : leads
    #     })
    #     return context 

    def get_queryset(self):
        user = self.request.user
        # Initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Category.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
          
        return queryset 

class UnassignedListView(LoginRequiredMixin, generic.ListView):
    template_name = "category_unassigned.html"
    context_object_name = "unassigned"

    def get_context_data(self, **kwargs):
        context = super(UnassignedListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
                
        context.update({
            "unassigned_leads" : queryset.filter(category__isnull=True)
        })

        return context 

    def get_queryset(self):
        user = self.request.user
    
        if user.is_organizer:
            queryset = Category.objects.filter(
                organisation = user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation = user.agent.organisation
            )

        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "lead_category_update.html"
    form_class = CategoryModelForm
    # context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter the agent that is logged in
            queryset = queryset.filter(agent__user=user)

        return queryset
    
    def get_success_url(self):
        return reverse('leads:lead_details', kwargs={"pk":self.get_object().id})

def landing_page(request):
    return render(request, 'landing_page.html')

def home(request):
    # return HttpResponse("Hello world")
    return render(request, 'home.html')

def leads(request):
    leads = Lead.objects.all()
    return render(request, 'lead_list.html', {"leads": leads})

def lead_details(request, pk):
    # print(pk)
    lead = Lead.objects.get(id=pk)
    # print(lead)
    return render(request, "lead_details.html", {"lead": lead})
# Model Form
def lead_create(request):
    form = LeadModelForm()
    # Crosschecking if the method is correct
    if request.method == "POST":
        # Parsing the data into the Lead form
        form = LeadModelForm(request.POST)
        # Verify and create a Lead with the data
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        "form": form
    } 
    return render(request, "lead_create.html", context)
    
def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        "lead": lead,
        "form": form
    }
    return render(request, 'lead_update.html', context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/")

# REFRENCE - How a simple update form works
# def leads_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm(instance=lead)
#     # Crosschecking if the method is correct
#     if request.method == "POST":
#         # Parsing the data into the Lead form
#         form = LeadForm(request.POST, instance=lead)
#         # Verify and create a Lead with the data
#         if form.is_valid():
#             # "form.cleaned_data" puts the data in a dict
#             firstname = form.cleaned_data['first_name']
#             lastname = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = firstname
#             lead.last_name = lastname
#             lead.age = age
#             lead.save()
#     context = {
#         "lead": lead,
#         "form": form
#     }
#     return render (request, "lead_update.html", context)

# REFERENCE - How a simply form works
# def leads_create(request):
#     form = LeadForm()
#     # Crosschecking if the method is correct
#     if request.method == "POST":
#         # Parsing the data into the Lead form
#         form = LeadForm(request.POST)
#         # Verify and create a Lead with the data
#         if form.is_valid():
#             # "form.cleaned_data" puts the data in a dict
#             firstname = form.cleaned_data['first_name']
#             lastname = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name= firstname,
#                 last_name = lastname,
#                 age = age,
#                 agent = agent
#             )
#             print('Lead has been created')
#             return redirect('/')
#     context = {
#         "form": form
#     } 
#     return render(request, "lead_create.html", context)