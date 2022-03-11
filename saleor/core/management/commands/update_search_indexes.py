from django.core.management.base import BaseCommand

from ....account.models import User
from ....order.models import Order
from ....product.models import Product
from ...search_tasks import (
    set_order_search_document_values,
    set_product_search_document_values,
    set_user_search_document_values,
)


class Command(BaseCommand):
    help = "Populate search indexes."

    def handle(self, *args, **options):
        # Update products
        products_total_count = Product.objects.filter(search_vector=None).count()
        self.stdout.write(f"Updating products: {products_total_count}")
        set_product_search_document_values.delay()

        # Update orders
        orders_total_count = Order.objects.filter(search_document="").count()
        self.stdout.write(f"Updating orders: {orders_total_count}")
        set_order_search_document_values.delay()

        # Update users
        users_total_count = User.objects.filter(search_document="").count()
        self.stdout.write(f"Updating users: {users_total_count}")
        set_user_search_document_values.delay()
