from django import forms
from apps.posts.models import Posts, PostsPreview


class PostForm(forms.ModelForm):
    tags = forms.CharField(max_length=500)

    class Meta:
        model = Posts
        exclude = ('user', 'tags', )

    def __init__(self, *args, **kwargs):

        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['prices'].widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['class'] = 'form-control'

    def save(self, **kwargs):
        user = kwargs.pop('user', False)
        type = kwargs.pop('type', False)
        proform = super(PostForm, self).save(commit = False, **kwargs)
        post = Posts()
        proform.user = user
        if type == 'buy':
           proform.buy_code = True
        elif type == 'sell':
           proform.sell_code = True
        else:
            pass
        proform.save()
        return proform

class PostPreviewForm(forms.ModelForm):
    tags = forms.CharField(max_length=500)

    class Meta:
        model = PostsPreview
        exclude = ('user', 'tags', 'preview')

    def __init__(self, *args, **kwargs):

        super(PostPreviewForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['prices'].widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['class'] = 'form-control'

    def save(self, **kwargs):
        user = kwargs.pop('user', False)
        type = kwargs.pop('type', False)
        posts = kwargs.pop('post', False)
        proform = super(PostPreviewForm, self).save(commit=False, **kwargs)
        post = PostsPreview()
        proform.user = user
        proform.preview = posts
        if type == 'buy':
           proform.buy_code = True
        elif type == 'sell':
           proform.sell_code = True
        else:
            pass
        proform.save()
        return proform

# class PostUpdateForm(forms.ModelForm):
#     tags = forms.CharField(max_length=500)
#
#     class Meta:
#         model = Posts
#         exclude = ('user', 'tags', )
#
#     def __init__(self, *args, **kwargs):
#
#         super(PostForm, self).__init__(*args, **kwargs)
#         self.fields['title'].widget.attrs['class'] = 'form-control'
#         self.fields['description'].widget.attrs['class'] = 'form-control'
#         self.fields['file'].widget.attrs['class'] = 'form-control'
#         self.fields['category'].widget.attrs['class'] = 'form-control'
#         self.fields['prices'].widget.attrs['class'] = 'form-control'
#         self.fields['tags'].widget.attrs['class'] = 'form-control'
#
#     def save(self, **kwargs):
#         user = kwargs.pop('user', False)
#         type = kwargs.pop('type', False)
#         proform = super(PostForm, self).save(commit = False, **kwargs)
#         post = Posts()
#         proform.user = user
#         if type == 'buy':
#            proform.buy_code = True
#         elif type == 'sell':
#            proform.sell_code = True
#         else:
#             pass
#         proform.save()
#         return proform
