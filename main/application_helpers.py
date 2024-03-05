import traceback
from uuid import UUID

from django.forms import ModelForm
from django.contrib import messages
from django.http import HttpRequest
#  from preferences import preferences

#  from core.helpers.debug_helpers import get_all_object_props, get_object_entry_names, get_object_entry_names_and_types, get_object_props
from core.helpers.logger import DEBUG
from core.helpers.utils import capitalize_id, getTrace

from .forms import ApplicationClientForm
from .models import Application, EventOption, Event
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


def save_application_options_from_post_data(request: HttpRequest, application: Application):
    """
    To call only for save objects?
    """
    try:
        # Get & update options list from post data...
        new_options_ids = request.POST.getlist('options')
        # Get suitable options for options' model QuerySet...
        # @see: https://docs.djangoproject.com/en/5.0/topics/db/queries/
        # pyright: ignore [reportAttributeAccessIssue]
        new_options = EventOption.objects.filter(id__in=new_options_ids,  # pyright: ignore [reportAttributeAccessIssue]
                                                 active=True)
        # Update many-to-many key (ManyRelatedManager) with a new options list...
        application.options.set(new_options)  # pyright: ignore [reportAttributeAccessIssue]
    except Exception as err:
        #  sError = errors.toString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        DEBUG(getTrace('save_application_options_from_post_data: Caught error'), {
            'err': err,
            'traceback': sTraceback,
        })


def get_and_update_application_from_request(
        request: HttpRequest,
        application_id: UUID | None = None,
        event_id: UUID | None = None):
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
        # Try to find an application if id passed...
        if application_id:
            check = Application.objects.filter(pk=application_id)  # pyright: ignore [reportAttributeAccessIssue]
            if check.exists():
                application = check[0]
                in_db = True
        # Create new (empty, with devault values) application if it's absent...
        if not application:
            application = Application()
            # Add event (?)
            if not application.event:
                if event_id:
                    application.event = Event.objects.get(pk=event_id)  # pyright: ignore [reportAttributeAccessIssue]
                else:
                    error_text = 'No event id provided to create a new application'
                    DEBUG(getTrace('get_and_update_application_from_request: error: ' + error_text), {
                        'error_text': error_text,
                    })
                    raise Exception(error_text)
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
                        DEBUG(getTrace('get_and_update_application_from_request: Email is in not allowed list'), {
                            'allowed_emails': allowed_emails,
                            'compare_email': compare_email,
                            'is_email_allowed': is_email_allowed,
                        })
                        messages.error(request, 'This email can not participate in the event, we are sorry.')

                # Check if current email is no_payment...
                no_payment_emails_str = event.no_payment_emails
                no_payment_emails = [s.strip(' ').lower() for s in no_payment_emails_str.split(',')]
                if len(no_payment_emails):
                    compare_email = cleaned_data['email'].lower()
                    is_email_no_payment = compare_email in no_payment_emails
                    if is_email_no_payment:
                        DEBUG(getTrace('get_and_update_application_from_request: Email is in no_payment list'), {
                            'no_payment_emails': no_payment_emails,
                            'compare_email': compare_email,
                            'is_email_no_payment': is_email_no_payment,
                        })
                        # Payment not required
                        application.payment_status = 'OK'

                DEBUG(getTrace('get_and_update_application_from_request: Saving data'), {
                    'allowed_emails': allowed_emails,
                    'application': application,
                    'cleaned_data': cleaned_data,
                    #  'allow_only_listed_emails': allow_only_listed_emails,
                })
                if doSave:
                    application.save()
                    save_application_options_from_post_data(request, application)
                    # TODO: Process the data in form.cleaned_data as required ... redirect to a new URL:
                    DEBUG(getTrace(
                        'get_and_update_application_from_request: Application successfully added: Redirect to application:edit_application'))
                    # Pass success nessage
                    updated = True
        # If no form created from request, then create and display form with a new one...
        if not form:
            # Create form...
            form = ApplicationClientForm(instance=application)
        context = {
            "form": form,
            "updated": updated,
            "in_db": in_db,
            "event_id": event_id,
        }
        # DEBUG
        if application:
            options = application.options.all()  # pyright: ignore [reportAttributeAccessIssue]
            option_ids = request.POST.getlist('options') if has_post_data else list(
                map(lambda item: str(item.id), options))
            if not application.event:
                error_text = 'No event propery in application object'
                DEBUG(getTrace('get_and_update_application_from_request: error'), {
                    'error_text': error_text,
                    'application': application,
                })
                raise Exception(error_text)
            event_options = application.event.options.filter(  # pyright: ignore [reportAttributeAccessIssue]
                active=True)
            DEBUG(getTrace('get_and_update_application_from_request: Result'), {
                'option_ids': option_ids,
                #  'options': options,
                #  'event_options': event_options,
                #  'context': context,
                'updated': updated,
                'in_db': in_db,
                'has_post_data': has_post_data,
                #  'form': form,
                #  'application': application,
            })
            context['option_ids'] = option_ids
            context['option_ids_joined'] = ','.join(option_ids) if option_ids else ''
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
