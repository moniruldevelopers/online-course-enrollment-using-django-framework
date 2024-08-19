# forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Enrollment, Contact

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['portal_screenshot', 'student_id','batch_no', 'transaction_id', 'phone_number', 'name', 'department', 'semester']

    course_price = forms.DecimalField(widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if course is set in the instance and has a price
        if self.instance.course_id and self.instance.course.price:
            self.fields['course_price'].initial = self.instance.course.price
        else:
            # Set a default value or handle this case as per your requirement
            self.fields['course_price'].initial = 0  # Set a default value (adjust as needed)

        # Mark phone_number field as required
        self.fields['phone_number'].required = True

        # Use crispy forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))




class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "name",
            "phone",
            "email",
            "message"
        ]
