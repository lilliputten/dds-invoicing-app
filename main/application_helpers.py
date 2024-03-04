import traceback

from django.forms import ModelForm
from django.contrib import messages
from django.http import HttpRequest
#  from preferences import preferences

#  from core.helpers.debug_helpers import get_all_object_props, get_object_entry_names, get_object_entry_names_and_types, get_object_props
from core.helpers.logger import DEBUG
from core.helpers.utils import capitalize_id, getTrace

from .forms import ApplicationClientForm
from .models import Application, EventOption
#  from .models import AllowedEmail


# @see:
# - https://docs.djangoproject.com/en/5.0/topics/db/queries/


def pass_form_errors_to_messages(request: HttpRequest, form: ModelForm):
    # TODO: Process dubplicated errors?
    errors = form.errors
    error_items = errors.items()  # pyright: ignore [reportOptionalMemberAccess]
    if len(error_items):
        # TODO: Show errors?
        # Data example: {'name': ['This field is required.'], 'email': ['This field is required.']}
        DEBUG(getTrace('Form has errors'))
        # 'error_items': error_items,  # NOTE: This dump causes TypeError: cannot pickle 'dict_items' object
        # 'errors': errors,  # NOTE: This dump is huge (`!!python/object/new:django.forms.utils.ErrorDict`)
        # Pass messages to client...
        for error, texts in error_items:  # pyright: ignore [reportOptionalMemberAccess]
            msg = capitalize_id(error) + ': ' + ' '.join(texts)
            messages.error(request, msg)


def get_and_update_application_from_request(request: HttpRequest, application_id: str | None = ''):
    """
    Create application and form:
    - From db if passed `application_id`.
    - From post request data if it's found.
    - Else create new application.
    If has post request data, then save created entry.
    """
    try:
        # Declare variables...
        updated = False
        in_db = False
        form = None
        application = None
        if application_id:
            # Try to find an application if id passed...
            try:
                application = Application.objects.get(pk=application_id)  # pyright: ignore [reportAttributeAccessIssue]
                if application:
                    in_db = True
            # DoesNotExist
            except Exception as err:
                sTraceback = str(traceback.format_exc())
                DEBUG(getTrace('get_and_update_application_from_request: Con not fetch an application'), {
                    'application_id': application_id,
                    'err': err,
                    'traceback': sTraceback,
                })
                #  raise err
                #  raise Http404("Application does not exist")
        # If request has posted form data...
        has_post_data = request.method == "POST"
        if has_post_data:
            # Create form from an existing object or/and post request data...
            form = ApplicationClientForm(request.POST, instance=application)
            DEBUG(getTrace('get_and_update_application_from_request: Created form'), {
                'application_id': application_id,
                'application': application,
            })
            # Is the form well-formed?
            if form.is_valid():
                doSave = True
                application = form.instance
                cleaned_data = form.cleaned_data
                # Get & update options list from post data...
                new_options_ids = request.POST.getlist('options')
                # Get suitable options for options' model QuerySet...
                # @see: https://docs.djangoproject.com/en/5.0/topics/db/queries/
                # pyright: ignore [reportAttributeAccessIssue]
                new_options = EventOption.objects.filter(id__in=new_options_ids, active=True)  # pyright: ignore [reportAttributeAccessIssue]
                # Update many-to-many key (ManyRelatedManager) with a new options list...
                application.options.set(new_options)

                # Get application's event...
                event = application.event

                # Check if current email is allowed...
                allowed_emails_str = event.allowed_emails
                allowed_emails = [s.strip(' ').lower() for s in allowed_emails_str.split(',')]
                if len(allowed_emails):
                    compare_email = cleaned_data['email'].lower()
                    is_email_allowed = compare_email in allowed_emails
                    if not is_email_allowed:
                        doSave = False
                        DEBUG(getTrace('get_and_update_application_from_request: Email is not allowed'), {
                            'allowed_emails': allowed_emails,
                            'compare_email': compare_email,
                            'is_email_allowed': is_email_allowed,
                        })
                        messages.error(request, 'This email can not participate in the event, we are sorry.')

                DEBUG(getTrace('get_and_update_application_from_request: Saving data'), {
                    'allowed_emails': allowed_emails,
                    'application': application,
                    'cleaned_data': cleaned_data,
                    #  'allow_only_listed_emails': allow_only_listed_emails,
                })
                if doSave:
                    application.save()
                    # TODO: Process the data in form.cleaned_data as required ... redirect to a new URL:
                    DEBUG(getTrace(
                        'get_and_update_application_from_request: Application successfully added: Redirect to application:edit_application'))
                    # Pass success nessage
                    updated = True
        # If no form created from request, then create and display form with a new one...
        if not form:
            # Create new application if absent...
            if not application:
                application = Application()
            # Create form...
            form = ApplicationClientForm(instance=application)
        context = {
            "form": form,
            "updated": updated,
            "in_db": in_db,
        }
        # DEBUG
        if application:
            options = application.options.all()  # pyright: ignore [reportAttributeAccessIssue]
            option_ids = list(map(lambda item: str(item.id), options))
            option_ids_joined = ','.join(option_ids)
            event_options = application.event.options.filter(  # pyright: ignore [reportAttributeAccessIssue]
                active=True)
            posted_options = request.POST.getlist('options') if has_post_data and 'options' in request.POST else None
            DEBUG(getTrace('get_and_update_application_from_request: Result'), {
                'option_ids': option_ids,
                #  'options': options,
                #  'event_options': event_options,
                #  'context': context,
                'updated': updated,
                'in_db': in_db,
                'has_post_data': has_post_data,
                'posted_options': posted_options,
                #  'form': form,
                #  'application': application,
            })
            context['option_ids'] = option_ids
            context['option_ids_joined'] = option_ids_joined
            context['event_options'] = event_options
        return (updated, in_db, form, application, context)
    except Exception as err:
        #  sError = errors.toString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        DEBUG(getTrace('get_and_update_application_from_request: Caught error'), {
            'err': err,
            'traceback': sTraceback,
        })
        raise err
