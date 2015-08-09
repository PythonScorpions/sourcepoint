from django import forms
from apps.accounts.models import *

class PlanForm(forms.ModelForm):

    class Meta:
        model = SubscriptionPlan
        fields = ['title', 'post_requirement', 'view_requirement', 'view_contact', 'show_interest',
                  'contact', 'free_plan']

    def __init__(self, *args, **kwargs):

        super(PlanForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'input-xlarge'
        self.fields['post_requirement'].widget.attrs['class'] = 'input-xlarge'
        self.fields['view_requirement'].widget.attrs['class'] = 'input-xlarge'
        self.fields['view_contact'].widget.attrs['class'] = 'input-xlarge'
        self.fields['show_interest'].widget.attrs['class'] = 'input-xlarge'

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):

        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'input-xlarge'

    def clean_name(self):
        category = self.cleaned_data.get("name",False)
        if Category.objects.filter(name=category).exists():
            raise forms.ValidationError("Category with the Same name already Exists")
        return category

class TagForm(forms.ModelForm):

     class Meta:
         model = TechnologyTags
         fields = ['tag']

     def __init__(self, *args, **kwargs):

        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['tag'].widget.attrs['class'] = 'input-xlarge'

     def clean_tag(self):
        tags = self.cleaned_data.get("tag",False)
        if TechnologyTags.objects.filter(tag=tags).exists():
            raise forms.ValidationError("Tag with the name already Exists")
        return tags


class AboutForm(forms.ModelForm):

    class Meta:
        model = AboutUs
        fields = ['site', 'banner', 'description', 'testimonial']

    def __init__(self, *args, **kwargs):

        super(AboutForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['class'] = 'cleditor'
        self.fields['testimonial'].widget.attrs['class'] = 'cleditor'


class OurTemaForm(forms.ModelForm):

    class Meta:
        model = OurTema
        fields = ['title', 'avatar', 'name', 'description']

    def __init__(self, *args, **kwargs):

        super(OurTemaForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['class'] = 'cleditor'


class WebSiteContentsForm(forms.ModelForm):

    class Meta:
        model = WebSiteContents
        fields = ['site', 'signin', 'signup']


    def __init__(self, *args, **kwargs):

        super(WebSiteContentsForm, self).__init__(*args, **kwargs)
        self.fields['signin'].widget.attrs['class'] = 'cleditor'
        self.fields['signup'].widget.attrs['class'] = 'cleditor'


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ['']





