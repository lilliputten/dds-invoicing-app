import traceback

from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.contrib import messages

# from core.helpers.debug_helpers import get_all_object_props, get_object_entry_names, get_object_entry_names_and_types, get_object_props
from core.helpers.logger import DEBUG
from core.helpers.utils import capitalize_id, getTrace

from .ApplicationForm import ApplicationClientForm
from .models import Application

"""
Save form:
    formset = ApplicationFormSet(request.POST)
"""


#  # Class-based template demo
#  class DetailView(generic.DetailView):
#      model = Application
#      template_name = "detail.html"


def components_demo(request: HttpRequest):
    return render(request, "components-demo.django")


def review_application(request: HttpRequest, application_id: str):
    # Find application by id...
    application = get_object_or_404(Application, pk=application_id)
    form = ApplicationClientForm(instance=application)
    context = {"application": application, "form": form}
    return render(request, "review-application.html.django", context)


def create_new_application(request: HttpRequest):
    try:
        #  raise Exception("Check exception")  # DEBUG
        form = None
        if request.method == "POST":
            form = ApplicationClientForm(request.POST)
            if form.is_valid():
                application = form.instance
                cleaned_data = form.cleaned_data
                DEBUG(getTrace('Saving data'), {
                    # 'form': form,
                    'application': application,
                    'cleaned_data': cleaned_data,
                })
                application.save()
                # TODO: Process the data in form.cleaned_data as required ... redirect to a new URL:
                DEBUG(getTrace('Application successfully added: Redirect to application:review_application'))
                # Pass success nessage
                messages.success(request, 'Application for email {} has successfully added.'.format(application.email))
                return redirect('application:review_application', application_id=application.id)
            else:
                errors = form.errors
                # TODO: Show errors?
                # Eg: {'name': ['This field is required.'], 'email': ['This field is required.']}
                DEBUG(getTrace('Form has errors'), {
                    # 'errors': errors,  # NOTE: This dump is huge (`!!python/object/new:django.forms.utils.ErrorDict`)
                })
                # Pass messages to client...
                for error, texts in form.errors.items():  # pyright: ignore [reportOptionalMemberAccess]
                    msg = capitalize_id(error) + ': ' + ' '.join(texts)
                    messages.error(request, msg)
        # If no form created from request, then create new one...
        DEBUG(getTrace('Render new form'))
        if not form:
            # Create empty application...
            application = Application()
            #  # DEBUG: Provide some test data for a fresh application...
            #  application.name = 'Test'  # pyright: ignore [reportAttributeAccessIssue]
            #  application.option_hackaton = True
            #  application.payment_method = 'INVOICE'
            #  application.save()
            form = ApplicationClientForm(instance=application)
        fields = form.fields
        context = {
            "form": form,
            #  # NOTE: These data are accessible via templatetags `form_field_type`, `form_select_choices`
            #  "field_types": {id: fields[id].widget.__class__.__name__ for id in fields},
            #  "select_choices": {id: fields[id].choices if fields[id].widget.__class__.__name__ == 'Select' else None
            #                     for id in fields},
        }
        DEBUG(getTrace('Rendering...'))
        return render(request, "new-application-form.html.django", context)
    except Exception as err:
        #  sError = errors.toString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        DEBUG(getTrace('Caught error'), {
            'err': err,
            'traceback': sTraceback,
        })
        raise err
        # TODO: Return error page
        #  return HttpResponse(status=500)


def index(request: HttpRequest):
    #  return HttpResponse("Hello, world. You're at the main index.")  # pyright: ignore [reportArgumentType]
    latest_application_list = Application.objects.order_by(  # pyright: ignore [reportAttributeAccessIssue]
        "-created_at")[:5]
    #  output = ", ".join([q.email for q in latest_application_list])
    #  return HttpResponse(output)
    context = {
        "latest_application_list": latest_application_list,
    }
    template = loader.get_template("index.html.django")
    return HttpResponse(template.render(context, request))


# Error pages...

def page403(request, *args, **argv):
    DEBUG(getTrace('403 error'), {
        'args': args,
        'argv': argv,
    })
    return render(request, '403.html', {}, status=403)


def page404(request, *args, **argv):
    DEBUG(getTrace('404 error'), {
        'args': args,
        'argv': argv,
    })
    return render(request, '404.html', {}, status=404)


def page500(request, *args, **argv):
    DEBUG(getTrace('500 error'), {
        'args': args,
        'argv': argv,
    })
    return render(request, '500.html', {}, status=500)


# Other errors:
# 502: Gateway Timeout
