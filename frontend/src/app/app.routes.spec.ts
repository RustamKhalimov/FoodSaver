import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of } from 'rxjs';

import { routes } from './app.routes';
import { AuthService, AuthUser } from './services/auth';
import { BarcodeScannerService } from './services/barcode-scanner';
import { DiscountRuleService } from './services/discount-rule';
import { ProductService } from './services/product';

describe('role-protected routes', () => {
  let user: AuthUser;
  const discountRules = {
    id: 1,
    enabled: true,
    two_days_discount: 20,
    one_day_discount: 30,
    expiry_day_discount: 50,
    updated_at: ''
  };

  beforeEach(() => {
    user = {
      id: 1,
      username: 'test-user',
      email: 'test@example.com',
      first_name: '',
      last_name: '',
      role: 'customer'
    };

    TestBed.configureTestingModule({
      providers: [
        provideRouter(routes),
        {
          provide: AuthService,
          useValue: {
            isLoggedIn: () => true,
            getProfile: () => of(user),
            removeToken: () => undefined,
            isAdmin: () => user.role === 'admin',
            isAuthenticated: () => true,
            authHeaders: () => undefined
          }
        },
        {
          provide: ProductService,
          useValue: {
            getProducts: () => of([]),
            getCatalog: () => of([]),
            getProduct: () => of({
              id: 1,
              name: 'Test',
              barcode: null,
              image_url: null,
              category: 'Other',
              expiry_date: null,
              quantity: 1,
              regular_price: 1,
              discount_percent: 0,
              discounted_price: 1,
              unit_size: null
            }),
            getExpiringProducts: () => of([]),
            addProduct: () => of({}),
            updateProduct: () => of({}),
            deleteProduct: () => of({})
          }
        },
        {
          provide: DiscountRuleService,
          useValue: {
            getRules: () => of(discountRules),
            updateRules: () => of(discountRules)
          }
        },
        { provide: BarcodeScannerService, useValue: {} }
      ]
    });
  });

  it('redirects customers away from Inventory and Rules URLs', async () => {
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/inventory');
    expect(TestBed.inject(Router).url).toBe('/discover');

    await harness.navigateByUrl('/rules');
    expect(TestBed.inject(Router).url).toBe('/discover');
  });

  it('allows admins to open Inventory and Rules', async () => {
    user.role = 'admin';
    const harness = await RouterTestingHarness.create();

    await harness.navigateByUrl('/inventory');
    expect(TestBed.inject(Router).url).toBe('/inventory');

    await harness.navigateByUrl('/rules');
    expect(TestBed.inject(Router).url).toBe('/rules');
  });
});
