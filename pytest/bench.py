from vaana_app import products
from fib import fib
from vaana_app.categories.tests.test_views import CategoryTest
from vaana_app.products.models import Product
from vaana_app.products.views import avg_rating
from vaana_app.users.models import UserManager
import pytest


def test_fib_10(benchmark):
    benchmark(fib, 10)


def test_fib_20(benchmark):
    benchmark(fib, 20)


def test_performance_categories(benchmark):
    benchmark(UserManager.create_user, "ed", "eddy@gmail.com",)
