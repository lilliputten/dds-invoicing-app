from django.forms import ModelForm

from .ApplicationModel import ApplicationModel


class ApplicationClientForm(ModelForm):
    asAdmin: bool = False

    #  # @see https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/
    #  def __init__(self, instance: ApplicationModel, asAdmin: bool = False):
    #      self.asAdmin = asAdmin
    #      super().__init__(instance=instance)

    class Meta:
        model = ApplicationModel
        exclude = ('id', 'secret_code', 'status', 'payment_status')
        fields = '__all__'


class ApplicationForm(ModelForm):
    asAdmin: bool = True

    #  # @see https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/
    #  def __init__(self, instance: ApplicationModel, asAdmin: bool = False):
    #      self.asAdmin = asAdmin
    #      super().__init__(instance=instance)

    class Meta:
        model = ApplicationModel
        exclude = ('id', 'secret_code')
        fields = '__all__'
