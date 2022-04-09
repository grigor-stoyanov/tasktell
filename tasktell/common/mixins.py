

class FormBootstrapMixin:
    def _init_bootstrap(self):
        for _, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            if not len(field.widget.attrs['class']):
                field.widget.attrs['class'] += 'form-control'

