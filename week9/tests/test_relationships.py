"""Lab 8 automated evidence: association, aggregation, composition, LSP, types."""

import contextlib
import io
import json
import tempfile
import unittest
from typing import get_type_hints
from pathlib import Path

from digital_product import DigitalProduct
from inventory import Inventory
from inventory_manager import load_inventory, save_inventory
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def show_product_details(product: Product) -> str:
    """One generic function supports every Product subtype without branching."""
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        product.display_information()
        print(product.get_fulfilment_info())
    return output.getvalue()


class Lab8Base(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("SUP-01", "Acme Supplies", "hello@acme.test")
        self.physical = PhysicalProduct("P-001", "Notebook", 12.50, 10,
                                        0.4, self.supplier)
        self.digital = DigitalProduct("D-001", "E-book", 7.99, 50,
                                      24.0, self.supplier)


class TestAssociation(Lab8Base):
    def test_one_supplier_is_shared_by_two_products(self) -> None:
        self.assertIs(self.physical.supplier, self.supplier)
        self.assertIs(self.digital.supplier, self.supplier)
        self.assertIsNot(self.physical, self.digital)

    def test_supplier_reference_survives_deleting_local_name(self) -> None:
        supplier = Supplier("SUP-X", "Independent", "team@independent.test")
        first = PhysicalProduct("P-X", "Pencil", 1.0, 3, 0.01, supplier)
        second = DigitalProduct("D-X", "Manual", 2.0, 3, 1.0, supplier)
        del supplier
        self.assertEqual(first.supplier.name, "Independent")
        self.assertIs(first.supplier, second.supplier)
        with contextlib.redirect_stdout(io.StringIO()) as captured:
            first.display_supplier_information()
            second.display_supplier_information()
        self.assertEqual(captured.getvalue().count("Supplier ID: SUP-X"), 2)

    def test_products_require_a_supplier_object(self) -> None:
        with self.assertRaises(TypeError):
            PhysicalProduct("P-X", "Pencil", 1.0, 3, 0.1, "SUP-01")


class TestAggregation(Lab8Base):
    def test_product_can_transfer_without_recreation(self) -> None:
        inventory_a = Inventory()
        inventory_b = Inventory()
        self.assertTrue(inventory_a.add_product(self.physical))
        self.assertIs(inventory_a.find_product("p-001"), self.physical)
        self.assertTrue(inventory_a.remove_product("P-001"))
        self.assertIsNone(inventory_a.find_product("P-001"))
        self.assertEqual(self.physical.name, "Notebook")
        self.assertTrue(inventory_b.add_product(self.physical))
        self.assertIs(inventory_b.find_product("P-001"), self.physical)

    def test_removing_unknown_product_returns_false(self) -> None:
        self.assertFalse(Inventory().remove_product("MISSING"))

    def test_inventory_rejects_duplicate_id(self) -> None:
        inventory = Inventory()
        self.assertTrue(inventory.add_product(self.physical))
        self.assertFalse(inventory.add_product(self.physical))

    def test_product_list_is_a_snapshot(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.products.clear()
        self.assertIs(inventory.find_product("P-001"), self.physical)


class TestComposition(Lab8Base):
    def test_orders_create_distinct_lines_but_share_product(self) -> None:
        first_order = Order("O-001")
        second_order = Order("O-002")
        first_order.add_order_line(self.physical, 2)
        second_order.add_order_line(self.physical, 3)
        first_line = first_order.order_lines[0]
        second_line = second_order.order_lines[0]
        self.assertIsNot(first_line, second_line)
        self.assertIs(first_line.product, second_line.product)
        self.assertIs(first_line.product, self.physical)

    def test_two_order_lines_and_total(self) -> None:
        order = Order("O-001")
        order.add_order_line(self.physical, 2)
        order.add_order_line(self.digital, 3)
        self.assertEqual(len(order.order_lines), 2)
        self.assertAlmostEqual(order.order_lines[0].calculate_subtotal(), 25.0)
        self.assertAlmostEqual(order.order_lines[1].calculate_subtotal(), 23.97)
        self.assertAlmostEqual(order.calculate_total(), 48.97)

    def test_removing_line_does_not_remove_product(self) -> None:
        order = Order("O-001")
        order.add_order_line(self.digital, 1)
        self.assertTrue(order.remove_order_line("D-001"))
        self.assertEqual(order.order_lines, [])
        self.assertEqual(self.digital.get_fulfilment_info(),
                         "Delivered digitally via download.")
        self.assertFalse(order.remove_order_line("D-001"))

    def test_order_list_is_not_externally_mutable(self) -> None:
        order = Order("O-001")
        order.add_order_line(self.physical, 1)
        order.order_lines.clear()
        self.assertEqual(len(order.order_lines), 1)

    def test_quantity_must_be_positive_integer(self) -> None:
        order = Order("O-001")
        for invalid in (-1, 0, 1.5, True):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                order.add_order_line(self.physical, invalid)


class TestLSPAndPolymorphism(Lab8Base):
    def test_same_function_accepts_both_product_types(self) -> None:
        physical_text = show_product_details(self.physical)
        digital_text = show_product_details(self.digital)
        self.assertIn("Requires physical shipping.", physical_text)
        self.assertIn("Delivered digitally via download.", digital_text)
        self.assertIn("Supplier: Acme Supplies", physical_text)

    def test_both_types_support_stock_updates(self) -> None:
        for product in (self.physical, self.digital):
            with self.subTest(product=product.product_id):
                product.update_stock(7)
                self.assertEqual(product.stock, 7)
                with self.assertRaises(ValueError):
                    product.update_stock(-1)

    def test_inventory_polymorphic_loop(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)
        with contextlib.redirect_stdout(io.StringIO()) as captured:
            for product in inventory.products:
                product.display_information()
                print(product.get_fulfilment_info())
        output = captured.getvalue()
        self.assertIn("Type: Physical", output)
        self.assertIn("Type: Digital", output)
        self.assertIn("Requires physical shipping.", output)
        self.assertIn("Delivered digitally via download.", output)

    def test_shipping_only_on_physical_product(self) -> None:
        self.assertAlmostEqual(self.physical.calculate_shipping_cost(), 4.80)
        self.assertFalse(hasattr(self.digital, "calculate_shipping_cost"))


class TestTypeHints(Lab8Base):
    def test_relationships_have_concrete_annotations(self) -> None:
        self.assertIs(get_type_hints(Product.__init__)["supplier"], Supplier)
        self.assertEqual(get_type_hints(Inventory.find_product)["return"], Product | None)
        self.assertEqual(get_type_hints(Order.add_order_line)["product"], Product)
        self.assertEqual(get_type_hints(OrderLine.calculate_subtotal)["return"], float)
        self.assertEqual(get_type_hints(Inventory.products.fget)["return"], list[Product])


class TestPersistence(Lab8Base):
    def test_round_trip_preserves_shared_supplier_identity(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)
        with tempfile.TemporaryDirectory() as folder:
            filename = str(Path(folder) / "inventory.json")
            self.assertTrue(save_inventory(inventory, filename))
            with open(filename, encoding="utf-8") as file:
                saved = json.load(file)
            self.assertEqual(saved[0]["supplier"]["supplier_id"], "SUP-01")
            with contextlib.redirect_stdout(io.StringIO()):
                restored = load_inventory(filename)
        self.assertIs(restored.find_product("P-001").supplier,
                      restored.find_product("D-001").supplier)
        self.assertEqual(len(restored.products), 2)

    def test_old_lab7_json_can_be_loaded_with_placeholder_supplier(self) -> None:
        previous_record = [{
            "id": "P-OLD", "name": "Eraser", "price": 1.50,
            "stock": 2, "type": "physical", "weight": 0.05,
        }]
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "inventory.json"
            filename.write_text(json.dumps(previous_record), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                restored = load_inventory(str(filename))
        self.assertEqual(restored.find_product("P-OLD").supplier.supplier_id,
                         "UNASSIGNED")

    def test_corrupt_json_does_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "inventory.json"
            filename.write_text("{broken", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                restored = load_inventory(str(filename))
        self.assertEqual(restored.products, [])


if __name__ == "__main__":
    unittest.main()
