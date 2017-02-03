For reading the ODS, XLS or XLSX file I use [pyexcel-ods](https://pypi.python.org/pypi/pyexcel-ods), [pyexcel-xls](https://pypi.python.org/pypi/pyexcel-xls) and [pyexcel-xlsx](https://pypi.python.org/pypi/pyexcel-xlsx).

In this example, I will describe how to parse a sheet with this structure:

![Sheet example](https://raw.githubusercontent.com/DMS86/dmunoz/master/img/sheet-example.png)

I also describe how to test the Upload Form using the Django Test Framework.

The logic is the following:

1. The user uploads the file.
2. The server stores it and decides which library will parse it. If extension is wrong, return.
3. Server checks if the sheet is complete according to the defined structure. In this example, I don't check if there is extra data.
4. Process the data.
5. Remove file from server and return

## urls.py

    from django.conf.urls import patterns, url

    import myapp.views as v

    urlpatterns = patterns('',
        url(r'^upload-file/', v.MyUploadFormView.as_view(), name='my_upload_form_view'),
        url(r'^success/', v.SuccessView.as_view(), name='success'),
        url(r'^failure/', v.FailureView.as_view(), name='failure'),
    )

We have three views: one to upload the file, one to redirect after success and one to redirect after failure.

## forms.py

First, you need to have a defined Form class in your `forms.py` file:

    class MyUploadForm(forms.Form):
        file = forms.FileField()

## views.py

Create a FormView in your `views.py` file:

    import os

    from django.conf import settings
    from django.contrib import messages
    from django.contrib.auth.models import User
    from django.core.urlresolvers import reverse, reverse_lazy
    from django.http import HttpResponseRedirect
    from django.views.generic.edit import FormView
    from pyexcel_ods import get_data as ods_get_data
    from pyexcel_xls import get_data as xls_get_data
    from pyexcel_xlsx import get_data as xlsx_get_data
    from myapp.forms import MyUploadForm

    class MyUploadFormView(FormView):
        template_name = 'my-template.html'
        form_class = MyUploadForm
        success_url = reverse_lazy('success')

        def form_valid(self, form, *args, **kwargs):
            # Write the file in a path
            f = form.cleaned_data['file']
            path = settings.MEDIA_ROOT + '/' + f.name
            with open(path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            # Check file extension and choose which library to use
            if f.name.endswith('.xlsx'):
                data = xlsx_get_data(path)
            elif f.name.endswith('.xls'):
                data = xls_get_data(path)
            elif f.name.endswith('.ods'):
                data = ods_get_data(path)
            else:
                os.remove(path)
                messages.info(self.request, 'File extension must be XLS, XLSX or ODS.')
                return HttpResponseRedirect(reverse('failure'))
            try:
                sheet = data['Sheet1']
            except:
                sheet = data['text to data sheet 1 in other language']
            # Check if sheet data is complete
            for i in range(1,len(sheet)):
                row_array = sheet[i]
                complete = True
                complete &= row_array[0] not in [None,'']
                complete &= row_array[1] not in [None,'']
                complete &= row_array[2] not in [None,'']
                complete &= row_array[3] not in [None,'']
                if not complete:
                    # Remove file and redirect to template,
                    # sending a message with django messages framework
                    os.remove(path)
                    messages.info(self.request, 'File info incomplete')
                    return HttpResponseRedirect(reverse('failure'))
            # Process data
            # Reading from row 1 because headers are in row 0
            for i in range(1,len(sheet)):
                row_array  = sheet[i]
                username   = unicode(row_array[0])
                first_name = unicode(row_array[1])
                last_name  = unicode(row_array[2])
                email      = unicode(row_array[3])

                # double check completeness
                if username and first_name and last_name and email:
                    User.objects.create_user(username, email, create_random_password(),
                        first_name=first_name, last_name=last_name)
            # Remove file and redirect to template,
            # sending a success message with django messages framework
            os.remove(path)
            messages.info(self.request, 'Success!')
            return HttpResponseRedirect(reverse('success'))

## tests.py

Create a test folder in your project's static folder. You need to create one correct data sheet and one incorrect data sheet for each file extension, and store them in the `$project_name$/static/test/` folder.

    import os

    from django.core.files.uploadedfile import InMemoryUploadedFile
    from django.core.urlresolvers import reverse
    from django.contrib.auth.models import User
    from django.templatetags.static import static
    from django.test import TestCase
    from io import BytesIO
    from myapp.forms import MyUploadForm

    class MyUploadFormTestCase(TestCase):

        # base method for testing correct ODS, XLS and XLSX file
        def my_upload_form_correct(self, filename, content_type):
            # sheet has 2 users, as in the image
            original_users = User.objects.all().count()

            # You need to store an example file in a folder to upload it
            BASE_DIR = os.path.dirname(os.path.dirname(__file__))
            path = BASE_DIR + '/project' + static(filename)
            upload_file = open(path, 'rb')

            # Create an UploadedFile based on the example uploaded file
            # These are the fields for creating it:
            # file, field_name, name, content_type, size, charset, content_type_extra=None
            imf = InMemoryUploadedFile(BytesIO(upload_file.read()), 'file', upload_file.name,
                content_type, os.path.getsize(path), None, {})
            file_dict = {'file': imf }
            form_data = {}
            form_data['file'] = imf
            form = MyUploadForm(form_data, file_dict)

            # assert valid form
            self.assertTrue(form.is_valid())

            # assert valid response redirect and message
            response = self.client.post(reverse('my_upload_form_view'), form_data, follow=True)
            self.assertRedirects(response, reverse('success'))
            messages = list(response.context['messages'])
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), 'Success!')

            # assert valid creation of objects
            self.assertEqual(original_users + 2, User.objects.all().count())
            self.assertTrue(User.objects.filter(username='dmunoz').exists())
            self.assertTrue(User.objects.filter(username='johndoe').exists())
            self.assertIsInstance(User.objects.get(username='dmunoz'), User)
            self.assertIsInstance(User.objects.get(username='johndoe'), User)

        def test_my_upload_form_correct_ods(self):
            self.my_upload_form_correct(
                'test/correctSheet.ods',
                'application/vnd.oasis.opendocument.spreadsheet')

        def test_my_upload_form_correct_xls(self):
            self.my_upload_form_correct(
                'test/correctSheet.xls',
                'application/vnd.ms-excel')

        def test_my_upload_form_correct_xlsx(self):
            self.my_upload_form_correct(
                'test/correctSheet.xlsx',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # base method for testing correct ODS, XLS and XLSX file
        def my_upload_form_incomplete(self, filename, content_type):
            # sheet has 2 users, as in the image
            original_users = User.objects.all().count()

            # You need to store an example file in a folder to upload it
            BASE_DIR = os.path.dirname(os.path.dirname(__file__))
            path = BASE_DIR + '/project' + static(filename)
            upload_file = open(path, 'rb')

            # Create an UploadedFile based on the example uploaded file
            # These are the fields for creating it:
            # file, field_name, name, content_type, size, charset, content_type_extra=None
            imf = InMemoryUploadedFile(BytesIO(upload_file.read()), 'file', upload_file.name,
                content_type, os.path.getsize(path), None, {})
            file_dict = {'file': imf }
            form_data = {}
            form_data['file'] = imf
            form = MyUploadForm(form_data, file_dict)

            # assert valid form
            self.assertTrue(form.is_valid())

            # assert valid response redirect and message
            response = self.client.post(reverse('my_upload_form_view'), form_data, follow=True)
            self.assertRedirects(response, reverse('failure'))
            messages = list(response.context['messages'])
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), 'File info incomplete')

        def test_my_upload_form_incomplete_ods(self):
            self.my_upload_form_incomplete(
                'test/incompleteSheet.ods',
                'application/vnd.oasis.opendocument.spreadsheet')

        def test_my_upload_form_incomplete_xls(self):
            self.my_upload_form_incomplete(
                'test/incompleteSheet.xls',
                'application/vnd.ms-excel')

        def test_my_upload_form_incomplete_xlsx(self):
            self.my_upload_form_incomplete(
                'test/incompleteSheet.xlsx',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        def test_my_upload_form_wrong_extension(self):
            # sheet has 2 users, as in the image
            original_users = User.objects.all().count()

            # You need to store an example file in a folder to upload it
            BASE_DIR = os.path.dirname(os.path.dirname(__file__))
            path = BASE_DIR + '/project' + static(filename)
            upload_file = open(path, 'rb')

            # Create an UploadedFile based on the example uploaded file
            # These are the fields for creating it:
            # file, field_name, name, content_type, size, charset, content_type_extra=None
            imf = InMemoryUploadedFile(BytesIO(upload_file.read()), 'file', upload_file.name,
                content_type, os.path.getsize(path), None, {})
            file_dict = {'file': imf }
            form_data = {}
            form_data['file'] = imf
            form = MyUploadForm(form_data, file_dict)

            # assert valid form
            self.assertTrue(form.is_valid())

            # assert valid response redirect and message
            response = self.client.post(reverse('my_upload_form_view'), form_data, follow=True)
            self.assertRedirects(response, reverse('failure'))
            messages = list(response.context['messages'])
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), 'File extension must be XLS, XLSX or ODS.')