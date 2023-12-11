from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.paginator import Paginator
from company_assistant.services.evaluator import Evaluator
from company_assistant.services.diagram_drawer import DiagramDrawer

from company_assistant.services.prioritizer import Prioritizer

from .models import Company, CompanySpecific, Specific, SwdProcess

from .forms import PracticeFormset, NewEmployerForm, NewCompanyForm

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
    if request.method == "POST":
        payload = {
            key.replace("attr-", ""): request.POST.getlist(key)
            for key in request.POST
            if key.startswith("attr-")
        }
        evaluator = Evaluator(
            company=company,
            practice_attributes=payload
        )
        sorted_practices = evaluator.prioritized_practices
        drawer = DiagramDrawer(prioritized_practices=sorted_practices)
        print(evaluator.evaluate())
        print(evaluator.process_scores)
        print(evaluator.practice_scores)
        drawer.plot_eval_score(evaluator.overall_score)
    else:
        prioritizer = Prioritizer(company=company)
        sorted_practices = prioritizer.get_sorted_by_practices()
        drawer = DiagramDrawer(prioritized_practices=sorted_practices)
    all_processes = SwdProcess.objects.all()  # TODO: allow specify processes to show
    practices_list = {
        process: PracticeFormset(instance=process)
        for process in all_processes
    }
    diagram = drawer.draw()
    return render(
        request=request,
        template_name='company_assistant/company_eval_page.html',
        context={
            'company': company,
            'sorted_practices': sorted_practices,
            'diagram': diagram,
            'practices_list': practices_list
        }
    )