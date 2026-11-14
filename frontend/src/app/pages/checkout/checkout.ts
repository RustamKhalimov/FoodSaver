import { DecimalPipe } from '@angular/common';
import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { Product, ProductService } from '../../services/product';
import {
  CartEntry,
  OrderService,
  ShoppingCartService
} from '../../services/shopping';

interface CheckoutLine extends CartEntry {
  product: Product | null;
}

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [DecimalPipe, RouterLink],
  templateUrl: './checkout.html',
  styleUrl: './checkout.css'
})
export class Checkout implements OnInit {
  private readonly productService = inject(ProductService);
  private readonly orderService = inject(OrderService);
  private readonly router = inject(Router);
  protected readonly cart = inject(ShoppingCartService);

  protected readonly products = signal<Product[]>([]);
  protected readonly loading = signal(true);
  protected readonly submitting = signal(false);
  protected readonly error = signal('');

  protected readonly lines = computed<CheckoutLine[]>(() => this.cart.entries()
    .map(entry => ({
      ...entry,
      product: this.products().find(product => product.id === entry.product_id) ?? null
    })));

  protected readonly total = computed(() => this.lines().reduce(
    (sum, line) => sum + (line.product
      ? Number(line.product.discounted_price) * line.quantity
      : 0),
    0
  ));

  protected readonly canPlaceOrder = computed(() =>
    !this.loading() &&
    !this.submitting() &&
    this.lines().length > 0 &&
    this.lines().every(line =>
      !!line.product &&
      line.product.quantity >= line.quantity &&
      this.isAvailable(line.product)
    )
  );

  ngOnInit(): void {
    this.productService.getProducts().subscribe({
      next: products => {
        this.products.set(products);
        this.loading.set(false);
      },
      error: error => {
        console.error('Checkout product loading error:', error);
        this.error.set('Unable to verify current stock and prices.');
        this.loading.set(false);
      }
    });
  }

  protected isAvailable(product: Product): boolean {
    return product.quantity > 0 &&
      (!product.expiry_date || product.expiry_date >= this.today());
  }

  protected placeOrder(): void {
    if (!this.canPlaceOrder()) return;

    this.submitting.set(true);
    this.error.set('');
    const items = this.cart.entries();

    this.orderService.placeOrder(items).subscribe({
      next: order => {
        this.cart.clear();
        this.router.navigate(['/orders', order.id], {
          queryParams: { confirmed: '1' }
        });
      },
      error: error => {
        console.error('Order placement failed:', error);
        this.error.set(
          error.error?.items ||
          error.error?.detail ||
          'Unable to place your order. Please review your cart and try again.'
        );
        this.submitting.set(false);
      }
    });
  }

  private today(): string {
    const now = new Date();
    return new Date(
      now.getTime() - now.getTimezoneOffset() * 60000
    ).toISOString().slice(0, 10);
  }
}
