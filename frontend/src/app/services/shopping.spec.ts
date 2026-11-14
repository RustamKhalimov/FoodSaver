import { TestBed } from '@angular/core/testing';
import { signal } from '@angular/core';

import { AuthService } from './auth';
import { ShoppingCartService } from './shopping';

describe('ShoppingCartService', () => {
  const currentUser = signal({ id: 93821 });

  beforeEach(() => {
    localStorage.clear();
    currentUser.set({ id: 93821 });
    TestBed.configureTestingModule({
      providers: [
        ShoppingCartService,
        {
          provide: AuthService,
          useValue: {
            currentUser,
            getUser: () => currentUser()
          }
        }
      ]
    });
  });

  it('persists quantities per user and supports update/remove/clear', () => {
    const cart = TestBed.inject(ShoppingCartService);

    cart.add(10, 2);
    cart.add(11, 1);
    expect(cart.itemCount()).toBe(3);

    cart.setQuantity(10, 4);
    expect(cart.itemCount()).toBe(5);
    expect(localStorage.getItem('foodsaver_cart_93821')).toContain('"quantity":4');

    cart.remove(11);
    expect(cart.entries()).toEqual([{ product_id: 10, quantity: 4 }]);

    cart.clear();
    expect(cart.itemCount()).toBe(0);
    expect(localStorage.getItem('foodsaver_cart_93821')).toBe('[]');
  });
});
