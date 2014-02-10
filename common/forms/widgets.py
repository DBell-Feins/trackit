from django.forms import widgets, ValidationError


class HeightWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        _widgets = (
            widgets.TextInput(),
            widgets.TextInput(),
        )
        super(HeightWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            feet = int(value/12)
            inches = int(value) - (feet * 12)
            return [feet, inches]
        return [None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        values = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        # ['5', '9'] - first number is feet, second is inches
        feet = values[0]
        inches = values[1]
        try:
            if int(inches) > 12:
                raise ValidationError('Invalid value')
            height = (int(feet) * 12) + int(inches)
        except ValueError:
            return ''
        return height
