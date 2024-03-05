import traceback
from uuid import UUID

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
from .models import Application, Event


"""
Save form:
    formset = ApplicationFormSet(request.POST)
"""


# Demo...


def components_demo(request: HttpRequest):
    return render(request, "components-demo.django")


# Information...


def generic_info(request: HttpRequest):
    try:
        application_id = request.session.get('application_id')  # pyright: ignore [reportAttributeAccessIssue]
        applications = Application.objects.filter(  # pyright: ignore [reportAttributeAccessIssue]
            pk=application_id) if application_id else None
        application = applications[0] if applications and len(applications) else None
        application_event = application.event if application else None
        events = Event.objects.all()  # pyright: ignore [reportAttributeAccessIssue]
        first_event = events[0] if events.exists() else None
        context = {
            'application_id': application_id,
            'first_event': first_event,
            'application': application,
            'application_event': application_event,
        }
        return render(request, "generic_info.html.django", context)
    except Exception as err:
        #  sError = errors.toString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        DEBUG(getTrace('show_application_state: Caught error'), {
            'err': err,
            'traceback': sTraceback,
        })
        raise err


def show_application_state(request: HttpRequest):
    try:
        application_id = request.session.get('application_id')  # pyright: ignore [reportAttributeAccessIssue]
        if not application_id:
            return redirect('application:default')
        applications = Application.objects.filter(pk=application_id)  # pyright: ignore [reportAttributeAccessIssue]
        if not applications.exists():
            return redirect('application:default')
        application = applications[0]
        context = {
            'application_id': application_id,
            'application': application,
        }
        return render(request, "show_application_state.html.django", context)
    except Exception as err:
        #  sError = errors.toString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        DEBUG(getTrace('show_application_state: Caught error'), {
            'err': err,
            'traceback': sTraceback,
        })
        raise err


# Activate applicaiton...


def activate_application(request: HttpRequest, application_id: UUID, secret_code: UUID):
    try:
        success = False
        application = None
        if not application_id or not secret_code:
            messages.error(request, 'Incorrect activation paramneters received')
        else:
            applications = Application.objects.filter(  # pyright: ignore [reportAttributeAccessIssue]
                pk=application_id,
                secret_code=secret_code,
                #  status='WAITING',
            )
            if not applications.exists():
                messages.error(request, 'No applications found for this link')
            else:
                application = applications[0]
                if application.status != 'WAITING':
                    messages.info(request, 'This application has already been activated')
                else:
                    # NOTE: Set 'ACTIVE' if pyament isn't required
                    application.status = 'ACTIVE' if application.payment_status == 'OK' else 'PAYMENT'
                    application.save()
                    # Send success message to the client...
                    messages.success(request, 'The application successfully activated')
                    # Save this application as 'current'...
                    request.session['application_id'] = str(  # pyright: ignore [reportAttributeAccessIssue]
                        application.id)
                    success = True
        context = {
            'application_id': application_id,
            'application': application,
            'success': success
        }
        # TODO: Redirect to the `show_application_state  for some cases?
        return render(request, 'activate_application.html.django', context)
    except Exception as err:
        #  sError = errors.toString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        DEBUG(getTrace('show_application_state: Caught error'), {
            'err': err,
            'traceback': sTraceback,
        })
        raise err


# Create application...


def edit_application(request: HttpRequest, application_id: UUID | None = None, event_id: UUID | None = None):
    try:
        (updated, in_db, form, application, context) = get_and_update_application_from_request(
            request, application_id=application_id, event_id=event_id)
        DEBUG(getTrace('edit_application: Result'), {
            'updated': updated,
            'in_db': in_db,
            # 'application': application,
            # 'form': form,
        })
        if updated and application:
            # Pass success nessage
            messages.success(
                request,
                'Application for email {} ({}) has successfully updated.'.format(
                    application.email,
                    application.name))
            request.session['application_id'] = str(  # pyright: ignore [reportAttributeAccessIssue]
                application.id)
            # TODO: Go to next state page?
            return redirect('application:show_application_state')  # , application_id=application.id)
        if not form:
            raise Exception('No application form found')
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


def create_new_application(request: HttpRequest, application_id: UUID | None = None, event_id: UUID | None = None):
    """
    Create new application for specified event.
    Go to generic info page if it hasn't specified.
    """
    try:
        if not event_id:
            DEBUG(getTrace('create_new_application: No event specified. Going to generic_info page.'))
            return redirect('application:default')
        (updated, in_db, form, application, context) = get_and_update_application_from_request(
            request, application_id=application_id, event_id=event_id)
        DEBUG(getTrace('create_new_application: Result'), {
            'updated': updated,
            'in_db': in_db,
            'application': application,
            #  'form': form,
        })
        # If application already updated...
        if updated and application:
            # Store application id into the session
            request.session['application_id'] = str(application.id)  # pyright: ignore [reportAttributeAccessIssue]
            # Pass success nessage
            messages.success(
                request,
                'Application for email {} ({}) has successfully added.'.format(
                    application.email,
                    application.name))
            # TODO: Go to next state page...
            return redirect('application:show_application_state')  # , application_id=application.id, event_id=event_id)
        # Else: no application updated...
        if not form:
            raise Exception('No application form found')
        pass_form_errors_to_messages(request, form)
        #  if request.method == "POST":
        #      DEBUG(getTrace('create_new_application: Redirecting to edit_application'))
        #      # Edit and update the application...
        #      return render(request, "edit_application.html.django", context)
        # Create new application...
        DEBUG(getTrace('create_new_application: Rendering new form'))
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


# Misc...


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
# 502: Gateway Timeout?
