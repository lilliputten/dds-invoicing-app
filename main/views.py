import traceback

from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import render
from django.contrib import messages
#  from django.core.mail import send_mail
from django.contrib.sites.models import Site
from preferences import preferences

from django.views.generic import TemplateView

#  from core.helpers.debug_helpers import get_all_object_props, get_object_entry_names, get_object_entry_names_and_types, get_object_props
from core.helpers.logger import DEBUG
from core.helpers.utils import getTrace

from .application_helpers import get_and_update_application_from_request, pass_form_errors_to_messages
from .models import Application


#  # DEMO: Using native django logger
#  import logging
#  LOG = logging.getLogger(__name__)
#  LOG.debug('Test', {
#      'allow_only_listed_emails': preferences.SitePreferences.allow_only_listed_emails,
#  })


"""
Save form:
    formset = ApplicationFormSet(request.POST)
"""


#  # DEMO: Class-based template demo
#  # Use as: ` path("application/<str:pk>/", views.DetailView.as_view(), name="detail")`
#  class DetailView(generic.DetailView):
#      model = Application
#      template_name = "detail.html"


def components_demo(request: HttpRequest):
    return render(request, "components-demo.django")


def edit_application(request: HttpRequest, application_id: str | None = ''):
    try:
        (updated, in_db, form, application) = get_and_update_application_from_request(request, application_id)
        DEBUG(getTrace('edit_application: Result'), {
            'updated': updated,
            'in_db': in_db,
            'application': application,
            #  'form': form,
        })
        if updated and application:
            # Pass success nessage
            messages.success(
                request,
                'Application for email {} ({}) has successfully updated.'.format(
                    application.email,
                    application.name))
            # TODO: Go to next state page?
            return redirect('application:edit_application', application_id=application.id)
        if not form:
            raise Exception('No application form found')
        context = {"form": form, "updated": updated, "in_db": in_db}
        pass_form_errors_to_messages(request, form)
        return render(request, "edit_application.html.django", context)
    except Exception as err:
        #  sError = errors.toString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        DEBUG(getTrace('edit_application: Caught error'), {
            'err': err,
            'traceback': sTraceback,
        })
        raise err
        #  TODO: Return error page
        #  raise Http500("Question does not exist")
        #  return HttpResponse(status=500)


def create_new_application(request: HttpRequest):
    try:
        (updated, in_db, form, application) = get_and_update_application_from_request(request)
        DEBUG(getTrace('create_new_application: Result'), {
            'updated': updated,
            'in_db': in_db,
            'application': application,
            #  'form': form,
        })
        # If application already updated...
        if updated and application:
            # Pass success nessage
            messages.success(
                request,
                'Application for email {} ({}) has successfully added.'.format(
                    application.email,
                    application.name))
            # TODO: Go to next state page...
            return redirect('application:edit_application', application_id=application.id)
        # Else: no application updated...
        if not form:
            raise Exception('No application form found')
        DEBUG(getTrace('create_new_application: Render new form'))
        context = {"form": form, "updated": updated, "in_db": in_db}
        pass_form_errors_to_messages(request, form)
        DEBUG(getTrace('create_new_application: Rendering...'))
        if request.method == "POST":
            return render(request, "edit_application.html.django", context)
        return render(request, "create_new_application.html.django", context)
    except Exception as err:
        #  sError = errors.toString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        DEBUG(getTrace('create_new_application: Caught error'), {
            'err': err,
            'traceback': sTraceback,
        })
        raise err
        #  TODO: Return error page
        #  raise Http500("Question does not exist")
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


class RobotsView(TemplateView):

    template_name = 'robots.txt'
    content_type = 'text/plain'

    def get_context_data(self, **kwargs):
        context = super(RobotsView, self).get_context_data(**kwargs)
        context['domain'] = Site.objects.get_current().domain
        return context

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
