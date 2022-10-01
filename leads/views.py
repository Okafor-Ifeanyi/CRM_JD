from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm

# Create your views here.
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