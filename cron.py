import os
from datetime import datetime, date
import pytz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discount_proj.settings')
import django
django.setup()
from basic_app.models import Order, Client, OrderStatus
from basic_app.views import calculate_bonuses


def close_orders_job():
    current_date = datetime.now(pytz.timezone('Asia/Yekaterinburg')).date()
    orders = Order.objects.filter(date_to=current_date)
    if orders:
        for order in orders:
            closed_status = OrderStatus.objects.get(order_status_name='Closed')
            if order.order_status.order_status_name == 'Active':
                bonuses = calculate_bonuses(order.date_from, order.date_to, order.price, order.bonuses_used)
                client = order.client
                client.bonuses += bonuses
                order.order_status = closed_status
                order.save()
                client.save()





close_orders_job()
