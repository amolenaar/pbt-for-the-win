from dataclasses import dataclass, field

from hypothesis import note, settings, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, initialize, Bundle


@dataclass(frozen=True)
class Product:
    name: str
    price: float


@dataclass
class LineItem:
    product: Product
    amount: int


@dataclass
class ShoppingCart:
    lines: list[LineItem] = field(default_factory=list)

    def add(self, product, amount):
        for line_item in self.lines:
            if line_item.product == product:
                line_item.amount += amount
                break
        else:
            self.lines.append(LineItem(product=product, amount=amount))

    def remove(self, product, amount):
        for line_item in self.lines:
            print(line_item.product, product)
            if line_item.product == product:
                if amount >= line_item.amount:
                    self.lines.remove(line_item)
                else:
                    line_item.amount -= amount

    @property
    def total(self):
        return sum(li.product.price * li.amount for li in self.lines)

    def __contains__(self, product):
        return any(li.product == product for li in self.lines)


def test_product_equality():
    product1 = Product("item", 2.0)
    product2 = Product("item", 2.0)
    
    assert product1 == product2
    assert product1 == product1


def test_remove_item():
    product = Product("item", 0.0)
    cart = ShoppingCart()
    cart.add(product, 1)
    cart.add(product, 1)
    

@settings(max_examples=200)
class Customer(RuleBasedStateMachine):

    def __init__(self):
        super().__init__()
        self.cart = ShoppingCart()
    
    Products = Bundle("products")

    @rule(target=Products, price=st.floats(min_value=1.0, max_value=100))
    def make_a_cart(self, price):
        return Product("item", price=price)

    @rule(product=Products, amount=st.integers(min_value=1, max_value=10))
    def add_line_item(self, product, amount):
        total_before = self.cart.total
        self.cart.add(product=product, amount=amount)
        assert total_before < self.cart.total

    @rule(product=Products, amount=st.integers(min_value=1, max_value=10))
    def remove_line_item(self, product, amount):
        total_before = self.cart.total
        self.cart.remove(product=product, amount=amount)
        assert total_before >= self.cart.total

    @invariant()
    def total_price(self):
        assert self.cart.total >= 0

    @invariant()
    def no_duplicate_products(self):
        unique_products_in_cart = set(li.product for li in self.cart.lines)
        assert len(unique_products_in_cart) == len(self.cart.lines), self.cart.lines


TestCase = Customer.TestCase
