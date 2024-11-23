from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

#Models
from ..models import m_centeroid

class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="Upload File Excel (.xlsx)")

class CenteroidForm(ModelForm):
    class Meta:
        model = m_centeroid
        fields = ["centeroid_type","jumlah_cluster", "max_perulangan"]
        labels = {
            "centeroid_type": _("Type Centeroid:"),
            "jumlah_cluster": _("Jumlah Cluster:"),
            "max_perulangan": _("Max Perulangan:"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mengatur widget dan label
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control",'required':True})

            self.fields[field].widget.attrs.update(
                {"data-label": self.fields[field].label}
            )

    def as_div(self):
        """Metode ini digunakan untuk merender form dengan div."""
        output = []
        for field in self:
            # Mendapatkan label dan field
            label = field.label_tag()  # Mendapatkan label sebagai HTML
            output.append(
                f'<div class="form-group row mb-2"><div class="col-sm-4">{label}</div><div class="col-sm-8">{field}</div></div>'
            )
        return "\n".join(output)
