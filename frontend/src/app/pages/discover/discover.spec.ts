import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';

import { Discover } from './discover';
import { ProductService } from '../../services/product';

describe('Discover', () => {
  const products = [
    {
      id: 1,
      name: 'Apple',
      barcode: null,
      image_url: null,
      category: 'Produce',
      expiry_date: '2026-11-16',
      quantity: 5,
      regular_price: 100,
      discount_percent: 20,
      discounted_price: 80,
      unit_size: null
    },
    {
      id: 2,
      name: 'Milk',
      barcode: null,
      image_url: null,
      category: 'Dairy',
      expiry_date: null,
      quantity: 3,
      regular_price: 200,
      discount_percent: 0,
      discounted_price: 200,
      unit_size: null
    }
  ];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Discover],
      providers: [
        provideRouter([]),
        {
          provide: ProductService,
          useValue: { getCatalog: () => of(products) }
        }
      ]
    }).compileComponents();
  });

  it('searches and filters products using catalog data', async () => {
    const fixture = TestBed.createComponent(Discover);
    fixture.detectChanges();
    await fixture.whenStable();

    const search = fixture.nativeElement.querySelector(
      'input[type="search"]'
    ) as HTMLInputElement;
    search.value = 'apple';
    search.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    await fixture.whenStable();

    let text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Apple');
    expect(text).not.toContain('Milk');

    search.value = '';
    search.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    await fixture.whenStable();

    const priceInputs = fixture.nativeElement.querySelectorAll(
      'input[type="number"]'
    ) as NodeListOf<HTMLInputElement>;
    priceInputs[1].value = '120';
    priceInputs[1].dispatchEvent(new Event('input'));
    fixture.detectChanges();
    await fixture.whenStable();

    text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Apple');
    expect(text).not.toContain('Milk');
  });
});
