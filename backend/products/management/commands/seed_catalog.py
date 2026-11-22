from datetime import timedelta
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone

from products.models import Product

PRODUCT_IMAGE_URLS = json.loads(
    Path(__file__).resolve().parents[2]
    .joinpath('product_images.json')
    .read_text(encoding='utf-8-sig')
)


PRODUCTS = [
    ('Avocado', 'Produce', 'FS20260001', 'Each', 650, 18, 'photo-1523049673857-eb18f1d7b578'),
    ('Baby Spinach', 'Produce', 'FS20260002', '125 g bag', 780, 12, 'photo-1576045057995-568f588f82fb'),
    ('Red Bell Peppers', 'Produce', 'FS20260003', '500 g pack', 990, 16, 'photo-1563565375-f3fdfdbefa83'),
    ('Broccoli Crowns', 'Produce', 'FS20260004', 'Each', 720, 17, 'photo-1459411552884-841db9b3cc2a'),
    ('Baby Potatoes', 'Produce', 'FS20260005', '1 kg bag', 850, 45, 'photo-1518977676601-b53f82aba655'),
    ('Lemons', 'Produce', 'FS20260006', '500 g bag', 680, 24, 'photo-1590502593747-42a996a2fb7f'),
    ('Blueberries', 'Produce', 'FS20260007', '125 g punnet', 1450, 10, 'photo-1498557850523-fd3d118b962e'),
    ('Strawberries', 'Produce', 'FS20260008', '250 g punnet', 1350, 11, 'photo-1464965911861-746a04b4bca6'),
    ('Green Pears', 'Produce', 'FS20260009', '1 kg', 880, 20, 'photo-1514756331096-242fdeb70d4a'),
    ('Button Mushrooms', 'Produce', 'FS20260010', '250 g tray', 790, 10, 'photo-1504545102780-26774c1bb073'),
    ('Mozzarella', 'Dairy', 'FS20260011', '200 g', 1250, 21, 'photo-1559561853-08451507cbe7'),
    ('Cottage Cheese', 'Dairy', 'FS20260012', '250 g tub', 890, 16, 'photo-1486297678162-eb2a19b0a32d'),
    ('Oat Milk', 'Dairy', 'FS20260013', '1 L carton', 1150, 35, 'photo-1550583724-b2692b85b150'),
    ('Vanilla Ice Cream', 'Dairy', 'FS20260014', '500 ml tub', 1650, 75, 'photo-1501446529957-6226bd447c46'),
    ('Sourdough Bagels', 'Bakery', 'FS20260015', '4 pack', 920, 11, 'photo-1549931319-a545dcf3bc73'),
    ('Multigrain Wraps', 'Bakery', 'FS20260016', '6 pack', 780, 24, 'photo-1565299624946-b28f40a0ae38'),
    ('Turkey Breast Slices', 'Meat', 'FS20260017', '250 g pack', 1850, 14, 'photo-1604503468506-a8da13d82791'),
    ('Salmon Fillet', 'Meat', 'FS20260018', '300 g pack', 3250, 10, 'photo-1519708227418-c8fd9a32b7a2'),
    ('Pork Chops', 'Meat', 'FS20260019', '500 g pack', 2800, 12, 'photo-1607623814075-e51df1bdc82f'),
    ('Firm Tofu', 'Other', 'FS20260020', '300 g pack', 950, 24, 'photo-1546069901-ba9599a7e63c'),
    ('Basmati Rice', 'Other', 'FS20260021', '1 kg bag', 1450, 300, 'photo-1586201375761-83865001e31c'),
    ('Penne Pasta', 'Other', 'FS20260022', '500 g pack', 620, 365, 'photo-1551462147-ff29053bfc14'),
    ('Extra Virgin Olive Oil', 'Other', 'FS20260023', '500 ml bottle', 3850, 450, 'photo-1474979266404-7eaacbcd87c5'),
    ('Roasted Almonds', 'Other', 'FS20260024', '200 g pack', 1750, 180, 'photo-1508061253366-f7da158b6d46'),
    ('Sparkling Water', 'Other', 'FS20260025', '1 L bottle', 490, 365, 'photo-1527960471264-932f39eb5846'),
    ('Whole Bean Coffee', 'Other', 'FS20260026', '250 g bag', 2650, 240, 'photo-1559056199-641a0ac8b55e'),
]

ADDITIONAL_PRODUCTS = [
    ('Yellow Onions', 'Produce', '1 kg bag', 520, 32),
    ('Garlic Bulbs', 'Produce', '3 pack', 430, 45),
    ('Zucchini', 'Produce', '500 g', 690, 16),
    ('Eggplant', 'Produce', 'Each', 760, 15),
    ('Cauliflower', 'Produce', 'Each', 980, 18),
    ('Red Cabbage', 'Produce', 'Each', 720, 28),
    ('Kale', 'Produce', '150 g bag', 850, 12),
    ('Romaine Lettuce', 'Produce', '2 heads', 890, 13),
    ('Sweet Corn', 'Produce', '2 ears', 640, 12),
    ('Green Beans', 'Produce', '300 g bag', 760, 12),
    ('Asparagus', 'Produce', '250 g bunch', 1450, 11),
    ('Celery Sticks', 'Produce', 'Each', 670, 18),
    ('Radishes', 'Produce', 'Bunch', 390, 11),
    ('Beets', 'Produce', '1 kg bag', 520, 35),
    ('Sweet Potatoes', 'Produce', '1 kg bag', 950, 32),
    ('Butternut Squash', 'Produce', 'Each', 1150, 40),
    ('Pumpkin Wedges', 'Produce', '500 g pack', 780, 16),
    ('Green Grapes', 'Produce', '500 g punnet', 1250, 12),
    ('Red Grapes', 'Produce', '500 g punnet', 1320, 12),
    ('Pineapple', 'Produce', 'Each', 1790, 18),
    ('Mangoes', 'Produce', '2 pack', 1480, 16),
    ('Kiwi Fruit', 'Produce', '4 pack', 980, 18),
    ('Peaches', 'Produce', '500 g punnet', 1190, 12),
    ('Nectarines', 'Produce', '500 g punnet', 1150, 12),
    ('Plums', 'Produce', '500 g punnet', 990, 12),
    ('Cherries', 'Produce', '300 g punnet', 1850, 10),
    ('Raspberries', 'Produce', '125 g punnet', 1650, 9),
    ('Blackberries', 'Produce', '125 g punnet', 1590, 9),
    ('Cantaloupe Melon', 'Produce', 'Each', 1450, 17),
    ('Watermelon', 'Produce', 'Each', 2490, 20),
    ('Grapefruit', 'Produce', 'Each', 570, 24),
    ('Limes', 'Produce', '4 pack', 690, 21),
    ('Fresh Basil', 'Produce', '30 g pack', 490, 10),
    ('Parsley Bunch', 'Produce', 'Bunch', 280, 10),
    ('Cilantro Bunch', 'Produce', 'Bunch', 280, 10),
    ('Whole Milk', 'Dairy', '1 L carton', 720, 18),
    ('Skim Milk', 'Dairy', '1 L carton', 690, 18),
    ('Lactose-Free Milk', 'Dairy', '1 L carton', 980, 22),
    ('Plain Kefir', 'Dairy', '900 ml bottle', 850, 15),
    ('Strawberry Yogurt', 'Dairy', '4 x 125 g', 920, 16),
    ('Blueberry Yogurt', 'Dairy', '4 x 125 g', 920, 16),
    ('Sour Cream', 'Dairy', '300 g tub', 740, 17),
    ('Heavy Cream', 'Dairy', '500 ml carton', 1350, 19),
    ('Whipping Cream', 'Dairy', '250 ml carton', 880, 18),
    ('Parmesan Cheese', 'Dairy', '180 g wedge', 1980, 35),
    ('Feta Cheese', 'Dairy', '200 g pack', 1420, 28),
    ('Gouda Cheese', 'Dairy', '250 g pack', 1850, 32),
    ('Cream Cheese', 'Dairy', '200 g tub', 1050, 24),
    ('Ricotta Cheese', 'Dairy', '250 g tub', 1250, 18),
    ('Swiss Cheese', 'Dairy', '200 g pack', 1780, 32),
    ('Provolone Cheese', 'Dairy', '200 g pack', 1690, 30),
    ('Brie Cheese', 'Dairy', '200 g wheel', 2250, 24),
    ('Condensed Milk', 'Dairy', '380 g can', 890, 180),
    ('Baguette', 'Bakery', 'Each', 480, 10),
    ('Rye Bread', 'Bakery', '500 g loaf', 690, 12),
    ('Ciabatta', 'Bakery', '400 g loaf', 750, 10),
    ('Pita Bread', 'Bakery', '6 pack', 620, 14),
    ('Flour Tortillas', 'Bakery', '8 pack', 780, 30),
    ('English Muffins', 'Bakery', '4 pack', 690, 18),
    ('Cinnamon Rolls', 'Bakery', '4 pack', 1250, 10),
    ('Chocolate Muffins', 'Bakery', '4 pack', 1180, 10),
    ('Blueberry Muffins', 'Bakery', '4 pack', 1180, 10),
    ('Seeded Crackers', 'Bakery', '200 g box', 820, 120),
    ('Oatmeal Cookies', 'Bakery', '250 g pack', 760, 90),
    ('Chocolate Chip Cookies', 'Bakery', '250 g pack', 790, 90),
    ('Fudge Brownies', 'Bakery', '4 pack', 1290, 12),
    ('Banana Bread', 'Bakery', '400 g loaf', 1150, 12),
    ('Plain Donuts', 'Bakery', '4 pack', 950, 9),
    ('Pretzel Buns', 'Bakery', '4 pack', 890, 14),
    ('Brioche Loaf', 'Bakery', '400 g loaf', 980, 14),
    ('Rosemary Focaccia', 'Bakery', '300 g loaf', 920, 10),
    ('Pizza Dough', 'Bakery', '500 g pack', 780, 20),
    ('Beef Sirloin Steak', 'Meat', '400 g pack', 4250, 12),
    ('Ribeye Steak', 'Meat', '350 g pack', 4980, 12),
    ('Lamb Chops', 'Meat', '500 g pack', 4650, 11),
    ('Ground Turkey', 'Meat', '500 g pack', 2350, 12),
    ('Chicken Thighs', 'Meat', '700 g pack', 2450, 12),
    ('Chicken Drumsticks', 'Meat', '700 g pack', 2180, 12),
    ('Chicken Wings', 'Meat', '600 g pack', 2250, 12),
    ('Pork Tenderloin', 'Meat', '500 g pack', 3150, 12),
    ('Pork Sausages', 'Meat', '400 g pack', 1980, 18),
    ('Beef Meatballs', 'Meat', '500 g pack', 2580, 18),
    ('Beef Brisket', 'Meat', '600 g pack', 3890, 12),
    ('Deli Ham', 'Meat', '200 g pack', 1450, 20),
    ('Beef Salami', 'Meat', '180 g pack', 1680, 24),
    ('Smoked Bacon', 'Meat', '250 g pack', 1890, 20),
    ('Frozen Shrimp', 'Meat', '400 g bag', 3250, 120),
    ('Cod Fillets', 'Meat', '400 g pack', 2950, 120),
    ('Tuna Steaks', 'Meat', '350 g pack', 3650, 120),
    ('Trout Fillet', 'Meat', '400 g pack', 3450, 12),
    ('Duck Breast', 'Meat', '400 g pack', 3980, 12),
    ('Spaghetti', 'Other', '500 g pack', 590, 365),
    ('Fusilli Pasta', 'Other', '500 g pack', 620, 365),
    ('Brown Rice', 'Other', '1 kg bag', 1180, 300),
    ('Quinoa', 'Other', '500 g bag', 1850, 240),
    ('Rolled Oats', 'Other', '1 kg bag', 980, 240),
    ('Corn Flakes', 'Other', '400 g box', 1250, 180),
    ('Honey Granola', 'Other', '350 g bag', 1480, 180),
    ('Wildflower Honey', 'Other', '350 g jar', 1950, 365),
    ('Maple Syrup', 'Other', '250 ml bottle', 2450, 365),
    ('Creamy Peanut Butter', 'Other', '340 g jar', 1380, 240),
    ('Tomato Pasta Sauce', 'Other', '500 g jar', 980, 240),
    ('Basil Pesto Sauce', 'Other', '190 g jar', 1290, 180),
    ('Chickpeas', 'Other', '400 g can', 490, 540),
    ('Black Beans', 'Other', '400 g can', 490, 540),
    ('Kidney Beans', 'Other', '400 g can', 490, 540),
    ('Coconut Milk', 'Other', '400 ml can', 720, 365),
    ('Vegetable Stock', 'Other', '1 L carton', 850, 180),
    ('Chicken Broth', 'Other', '1 L carton', 890, 180),
    ('Sea Salt', 'Other', '250 g jar', 520, 900),
    ('Black Pepper', 'Other', '80 g jar', 650, 900),
    ('Smoked Paprika', 'Other', '70 g jar', 690, 900),
    ('Curry Powder', 'Other', '70 g jar', 620, 900),
    ('Dried Oregano', 'Other', '25 g jar', 450, 900),
    ('Sunflower Seeds', 'Other', '200 g bag', 680, 180),
    ('Chia Seeds', 'Other', '200 g bag', 890, 240),
    ('Cashews', 'Other', '200 g bag', 1580, 180),
    ('Walnuts', 'Other', '200 g bag', 1450, 180),
    ('Green Tea Bags', 'Other', '20 tea bags', 790, 365),
    ('Hot Cocoa Mix', 'Other', '300 g tin', 1120, 240),
]

PHOTO_POOLS = {
    'Produce': [
        'photo-1523049673857-eb18f1d7b578',
        'photo-1576045057995-568f588f82fb',
        'photo-1563565375-f3fdfdbefa83',
        'photo-1459411552884-841db9b3cc2a',
        'photo-1498557850523-fd3d118b962e',
        'photo-1464965911861-746a04b4bca6',
    ],
    'Dairy': [
        'photo-1559561853-08451507cbe7',
        'photo-1486297678162-eb2a19b0a32d',
        'photo-1550583724-b2692b85b150',
        'photo-1501446529957-6226bd447c46',
        'photo-1505576399274-565b52d4ac71',
    ],
    'Bakery': [
        'photo-1549931319-a545dcf3bc73',
        'photo-1509440159596-0249088772ff',
        'photo-1530610476181-d83430b64dcd',
    ],
    'Meat': [
        'photo-1604503468506-a8da13d82791',
        'photo-1519708227418-c8fd9a32b7a2',
        'photo-1607623814075-e51df1bdc82f',
    ],
    'Other': [
        'photo-1546069901-ba9599a7e63c',
        'photo-1586201375761-83865001e31c',
        'photo-1551462147-ff29053bfc14',
        'photo-1474979266404-7eaacbcd87c5',
        'photo-1508061253366-f7da158b6d46',
        'photo-1559056199-641a0ac8b55e',
    ],
}


def unsplash_url(photo_id):
    return f'https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=900&q=85'


class Command(BaseCommand):
    help = 'Add a varied, duplicate-safe sample grocery catalog and refresh near expiry dates.'

    def handle(self, *args, **options):
        today = timezone.localdate()
        refresh_before = today + timedelta(days=7)
        changed_dates = 0

        for product in Product.objects.filter(expiry_date__isnull=False):
            if product.expiry_date <= refresh_before:
                product.expiry_date = today + timedelta(days=30)
                product.save(update_fields=['expiry_date', 'updated_at'])
                changed_dates += 1

        repaired_images = 0
        for product in Product.objects.all():
            image_url = PRODUCT_IMAGE_URLS.get(product.name)
            if not image_url or product.image_url == image_url:
                continue
            product.image_url = image_url
            product.save(update_fields=['image_url', 'updated_at'])
            repaired_images += 1

        existing_names = {
            name.casefold() for name in Product.objects.values_list('name', flat=True)
        }
        created = 0
        for name, category, barcode, unit_size, price, days, photo_id in PRODUCTS:
            if name.casefold() in existing_names:
                continue
            Product.objects.create(
                name=name,
                barcode=barcode,
                image_url=PRODUCT_IMAGE_URLS.get(name, unsplash_url(photo_id)),
                category=category,
                quantity=12,
                regular_price=price,
                unit_size=unit_size,
                expiry_date=today + timedelta(days=days),
            )
            existing_names.add(name.casefold())
            created += 1

        for index, (name, category, unit_size, price, days) in enumerate(
            ADDITIONAL_PRODUCTS,
            start=27,
        ):
            if name.casefold() in existing_names:
                continue
            photo_ids = PHOTO_POOLS[category]
            Product.objects.create(
                name=name,
                barcode=f'FS2026{index:04d}',
                image_url=PRODUCT_IMAGE_URLS.get(
                    name,
                    unsplash_url(photo_ids[index % len(photo_ids)]),
                ),
                category=category,
                quantity=12,
                regular_price=price,
                unit_size=unit_size,
                expiry_date=today + timedelta(days=days),
            )
            existing_names.add(name.casefold())
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Added {created} products; repaired {repaired_images} image links; '
            f'refreshed {changed_dates} near or past expiry dates; '
            f'catalog now has {Product.objects.count()} products.'
        ))
