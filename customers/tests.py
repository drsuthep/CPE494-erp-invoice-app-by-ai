import os
import re
from django.test import TestCase
from django.urls import reverse
from django.db.models import CharField, TextField, EmailField

from .models import Customer

class CustomerAppTests(TestCase):
    """Test suite for the customer app."""

    def setUp(self):
        """Set up initial data for tests."""
        self.valid_customer_data = {
            'code': 'CUST-001',
            'name': 'Test Customer Inc.',
            'address_line_1': '123 Main St',
            'address_line_2': 'Suite 4B',
            'city': 'Testville',
            'province': 'State',
            'country': 'Country',
            'postal_code': '12345',
            'phone': '555-1234',
            'email': 'test@customer.com',
            'notes': 'A test customer.'
        }

    def test_customer_model_fields(self):
        """Customer._meta.get_fields() includes all expected fields with correct types and constraints."""
        field_map = {f.name: f for f in Customer._meta.get_fields()}
        
        self.assertIn('id', field_map)
        self.assertIn('code', field_map)
        self.assertIn('name', field_map)
        self.assertIn('address_line_1', field_map)
        self.assertIn('address_line_2', field_map)
        self.assertIn('city', field_map)
        self.assertIn('province', field_map)
        self.assertIn('country', field_map)
        self.assertIn('postal_code', field_map)
        self.assertIn('phone', field_map)
        self.assertIn('email', field_map)
        self.assertIn('notes', field_map)
        self.assertIn('updated_at', field_map)

        code_field = field_map['code']
        self.assertTrue(code_field.unique)
        self.assertEqual(code_field.max_length, 32)
        
        name_field = field_map['name']
        self.assertFalse(name_field.blank)
        self.assertEqual(name_field.max_length, 200)

        notes_field = field_map['notes']
        self.assertIsInstance(notes_field, TextField)

        email_field = field_map['email']
        self.assertIsInstance(email_field, EmailField)

    def test_navbar_has_master_dropdown(self):
        """GET / response contains 'Master', 'Customer', 'Product'."""
        response = self.client.get(reverse('landing'))
        self.assertContains(response, 'Master')
        self.assertContains(response, 'Customer')
        self.assertContains(response, 'Product')

    def test_navbar_has_transactions_dropdown(self):
        """GET / response contains 'Transactions', 'Invoice'."""
        response = self.client.get(reverse('landing'))
        self.assertContains(response, 'Transactions')
        self.assertContains(response, 'Invoice')

    def test_customer_list_placeholder_renders(self):
        """GET /customers/ returns 200 and contains 'href="/customers/new/"'."""
        response = self.client.get(reverse('customers:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Customers')
        self.assertContains(response, f'href="{reverse("customers:create")}"')

    def test_customer_form_renders_all_fields(self):
        """GET /customers/new/ returns 200 and contains inputs for all 11 fields."""
        response = self.client.get(reverse('customers:create'))
        self.assertEqual(response.status_code, 200)
        for field in self.valid_customer_data.keys():
            self.assertContains(response, f'name="{field}"')

    def test_customer_form_required_asterisks(self):
        """GET /customers/new/ response contains '<span class="text-danger">*</span>' near 'code' and 'name' labels."""
        response = self.client.get(reverse('customers:create'))
        self.assertContains(response, '<span class="text-danger">*</span>', count=2)
        self.assertRegex(response.content.decode(), r'<label for="id_code">.*<span class="text-danger">\*</span></label>')
        self.assertRegex(response.content.decode(), r'<label for="id_name">.*<span class="text-danger">\*</span></label>')

    def test_customer_create_valid_redirects_to_edit(self):
        """POST /customers/new/ with valid data returns 302 to '/customers/\\d+/edit/'."""
        response = self.client.post(reverse('customers:create'), data=self.valid_customer_data)
        self.assertEqual(Customer.objects.count(), 1)
        customer = Customer.objects.first()
        self.assertRedirects(response, reverse('customers:edit', args=[customer.id]))

    def test_customer_create_save_flash_in_messages(self):
        """After valid POST, follow redirect and assert response contains 'Save successful'."""
        response = self.client.post(reverse('customers:create'), data=self.valid_customer_data, follow=True)
        self.assertContains(response, "Saving... Save successful")

    def test_customer_create_invalid_re_renders(self):
        """POST /customers/new/ with empty code returns 200, Customer.objects.count() == 0, and response contains 'invalid-feedback'."""
        invalid_data = self.valid_customer_data.copy()
        invalid_data['code'] = ''
        response = self.client.post(reverse('customers:create'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 0)
        self.assertContains(response, 'invalid-feedback')

    def test_customer_code_uniqueness(self):
        """Create customer with code='DUPE', then POST another with same code; second response is 200 and Customer.objects.filter(code='DUPE').count() == 1."""
        Customer.objects.create(code='DUPE', name='First Customer')
        self.assertEqual(Customer.objects.count(), 1)
        
        data = self.valid_customer_data.copy()
        data['code'] = 'DUPE'
        response = self.client.post(reverse('customers:create'), data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.filter(code='DUPE').count(), 1)
        self.assertContains(response, 'Customer with this Code already exists.')

    def test_customer_edit_loads_existing(self):
        """GET /customers/<id>/edit/ response contains the customer's data in form values."""
        customer = Customer.objects.create(**self.valid_customer_data)
        response = self.client.get(reverse('customers:edit', args=[customer.id]))
        self.assertContains(response, f'value="{customer.code}"')
        self.assertContains(response, f'value="{customer.name}"')
        self.assertContains(response, customer.notes)

    def test_customer_edit_save_persists(self):
        """POST /customers/<id>/edit/ with modified name; check database for updated value."""
        customer = Customer.objects.create(**self.valid_customer_data)
        updated_data = self.valid_customer_data.copy()
        updated_data['name'] = 'Updated Customer Name'
        
        response = self.client.post(reverse('customers:edit', args=[customer.id]), data=updated_data)
        self.assertRedirects(response, reverse('customers:edit', args=[customer.id]))
        
        customer.refresh_from_db()
        self.assertEqual(customer.name, 'Updated Customer Name')

    def test_customer_delete_removes_record(self):
        """POST /customers/<id>/delete/ returns 302; Customer.objects.filter(pk=id).exists() is False."""
        customer = Customer.objects.create(**self.valid_customer_data)
        self.assertTrue(Customer.objects.filter(pk=customer.id).exists())
        
        response = self.client.post(reverse('customers:delete', args=[customer.id]))
        self.assertRedirects(response, reverse('customers:list'))
        self.assertFalse(Customer.objects.filter(pk=customer.id).exists())

    def test_customer_delete_get_returns_405(self):
        """GET /customers/<id>/delete/ returns 405."""
        customer = Customer.objects.create(**self.valid_customer_data)
        response = self.client.get(reverse('customers:delete', args=[customer.id]))
        self.assertEqual(response.status_code, 405)

    def test_customer_form_has_close_button(self):
        """GET /customers/new/ contains '<a ... href="/customers/".*title="Close"'."""
        response = self.client.get(reverse('customers:create'))
        self.assertRegex(response.content.decode(), f'<a[^>]+href="{re.escape(reverse("customers:list"))}"[^>]+title="Close"')

    def test_customer_edit_form_has_delete_button(self):
        """GET /customers/<id>/edit/ contains '<button ... data-action="delete"'."""
        customer = Customer.objects.create(**self.valid_customer_data)
        
        # Edit form should have delete button
        response_edit = self.client.get(reverse('customers:edit', args=[customer.id]))
        self.assertContains(response_edit, 'data-action="delete"')
        
        # Create form should not have delete button
        response_create = self.client.get(reverse('customers:create'))
        self.assertNotContains(response_create, 'data-action="delete"')

    def test_placeholder_pages_render(self):
        """GET requests to /products/, /products/new/, /invoices/, /invoices/new/ all return 200."""
        urls = [
            reverse('products_list'),
            reverse('products_create'),
            reverse('invoices_list'),
            reverse('invoices_create'),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_placeholder_form_has_only_close(self):
        """GET /products/new/ response has one 'Close' button and no 'Save' button."""
        urls = [
            reverse('products_create'),
            reverse('invoices_create'),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, 'title="Close"')
                self.assertNotContains(response, 'title="Save"')
                self.assertNotContains(response, 'data-action="delete"')

    def test_no_thai_rendered_pages(self):
        """GET responses for all new pages do not contain characters in Unicode range U+0E00-U+0E7F."""
        thai_pattern = re.compile(r'[\u0e00-\u0e7f]')
        urls = [
            reverse('landing'),
            reverse('customers:list'),
            reverse('customers:create'),
            reverse('products_list'),
            reverse('products_create'),
            reverse('invoices_list'),
            reverse('invoices_create'),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                content = response.content.decode('utf-8')
                self.assertIsNone(thai_pattern.search(content), f"Thai characters found in {url}")

    def test_no_thai_generated_files(self):
        """Scan all generated files for this sprint; assert no characters in Unicode range U+0E00-U+0E7F."""
        thai_pattern = re.compile(r'[\u0e00-\u0e7f]')
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        files_to_check = [
            'customers/__init__.py', 'customers/apps.py', 'customers/models.py',
            'customers/forms.py', 'customers/views.py', 'customers/urls.py',
            'customers/admin.py', 'customers/tests.py',
            'erp_invoice/urls.py', 'erp_invoice/settings.py',
            'templates/base.html', 'templates/landing.html',
            'templates/customers/list_placeholder.html', 'templates/customers/form.html',
            'templates/placeholders/products_list.html', 'templates/placeholders/products_form.html',
            'templates/placeholders/invoices_list.html', 'templates/placeholders/invoices_form.html',
        ]

        for file_path_rel in files_to_check:
            file_path_abs = os.path.join(project_root, file_path_rel.replace('/', os.sep))
            if not os.path.exists(file_path_abs):
                # Some files might not exist yet in the test runner's context, skip them.
                # This test is more of a safety check.
                continue
            
            with self.subTest(file=file_path_rel):
                try:
                    with open(file_path_abs, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.assertIsNone(thai_pattern.search(content), f"Thai characters found in {file_path_rel}")
                except FileNotFoundError:
                    self.fail(f"File not found for Thai character check: {file_path_abs}")
                except Exception as e:
                    self.fail(f"Error reading file {file_path_abs}: {e}")