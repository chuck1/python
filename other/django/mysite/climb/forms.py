import django.forms

import climb.models

class route_select(django.forms.Form):
    route = django.forms.ModelChoiceField(
            queryset=climb.models.Route.objects.all())

class pitch_widget(django.forms.Widget):
    """
    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    """
    input_type = "text"  # Subclasses must define this.

    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))

        form = route_select()

        s0 = unicode(route_select.route)
        s1 = django.utils.html.format_html('<input{} />', django.forms.utils.flatatt(final_attrs))

        return s0

class route_create(django.forms.Form):
    name   = django.forms.CharField(max_length=256)
    wall   = django.forms.ModelChoiceField(
            queryset=climb.models.Wall.objects.all())
   
class climb_create(django.forms.Form):
    date   = django.forms.DateField()

    location = django.forms.ModelChoiceField(
            queryset=climb.models.Location.objects.all())
    area     = django.forms.ModelChoiceField(
            queryset=climb.models.Area.objects.all())
    wall     = django.forms.ModelChoiceField(
            queryset=climb.models.Wall.objects.all())
    route    = django.forms.ModelChoiceField(
            queryset=climb.models.Route.objects.all())
    pitch    = django.forms.ModelChoiceField(
            queryset=climb.models.Pitch.objects.all())
    


