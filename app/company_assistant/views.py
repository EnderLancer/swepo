from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.paginator import Paginator

from .models import Company, CompanySpecific, Specific

from .forms import NewEmployerForm, NewCompanyForm

def authorization_with_login(view):
    def auth_awared_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You should be authorized for such actions" )
            return redirect("login")
        return view(request, *args, **kwargs)
    return auth_awared_view


def register_request(request):
    if request.method == "POST":
        form = NewEmployerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewEmployerForm()
    return render(request=request, template_name="company_assistant/register.html", context={"register_form":form})


def home(request):
    return render(request=request, template_name="company_assistant/home.html")

@authorization_with_login
def company_list(request):
    companies = Company.objects.filter(created_by__user_id=request.user.id)
    paginator = Paginator(companies, 10)  # Display 10 companies per page
    page = request.GET.get('page')
    companies = paginator.get_page(page)
    return render(
        request=request,
        template_name='company_assistant/company_list.html',
        context={'companies': companies}
    )

@authorization_with_login
def company_create(request):
    if request.method == "POST":
        form = NewCompanyForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user.employer
            form.save()
            return redirect("company_list")

    form = NewCompanyForm()
    return render(
        request=request,
        template_name='company_assistant/company_create.html',
        context={'form': form}
    )


@authorization_with_login
def company_view(request, company_id: int):
    company = Company.objects.get(id=company_id)
    company_specifics = company.specifics.through.objects.all()
    return render(
        request=request,
        template_name='company_assistant/company_view.html',
        context={
            'company': company,
            'company_specifics': company_specifics,
        }
    )


@authorization_with_login
def company_specifics_change(request, company_id: int):
    company = Company.objects.get(id=company_id)
    company_specifics = company.specifics.through.objects.all()

    if request.method == "POST":
        SPECIFIC_PREFIX = "specific_"
        post_fields = request.POST
        to_create = []
        for key, value in post_fields.items():
            if (
                key.startswith(SPECIFIC_PREFIX)
                and value != "None"
                and 1 < int(value) < 5
            ):
                to_create.append(
                    CompanySpecific(
                        company=company,
                        specific_id=int(key.replace(SPECIFIC_PREFIX, "")),
                        score=int(value)
                    )
                )
        CompanySpecific.objects.bulk_create(to_create)
        return redirect("company_specifics_change", company_id=company_id)

    unassigned_specifics = Specific.objects.exclude(id__in=company.specifics.values_list("id", flat=True))
    return render(
        request=request,
        template_name='company_assistant/company_specifics_change.html',
        context={
            'company': company,
            'company_specifics': company_specifics,
            'unassigned_specifics': unassigned_specifics,
        }
    )

def company_eval_view(request, company_id):
    company = Company.objects.get(id=company_id)
    return render(
        request=request,
        template_name='company_assistant/company_specifics_change.html',
        context={
            'company': company,
        }
    )