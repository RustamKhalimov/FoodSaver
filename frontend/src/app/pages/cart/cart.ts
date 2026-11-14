import { DecimalPipe } from '@angular/common';
import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { Product, ProductService } from '../../services/product';
import { CartEntry, ShoppingCartService } from '../../services/shopping';

interface CartLine extends CartEntry {
  product: Product | null;
}

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [DecimalPipe, RouterLink],
  templateUrl: './cart.html',
  styleUrl: './cart.css'
})
export class Cart implements OnInit {
  private readonly productService = inject(ProductService);
  protected readonly cart = inject(ShoppingCartService);

  protected readonly products = signal<Product[]>([]);
  protected readonly loading = signal(true);
  protected readonly error = signal('');

  protected readonly lines = computed<CartLine[]>(() => this.cart.entries()
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

  protected readonly canCheckout = computed(() =>
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
        console.error('Cart product loading error:', error);
        this.error.set('Unable to load current product prices and stock.');
        this.loading.set(false);
      }
    });
  }

  protected setQuantity(productId: number, quantity: number): void {
    const product = this.products().find(item => item.id === productId);
    if (!product) return;
    this.cart.setQuantity(
      productId,
      Math.max(1, Math.min(product.quantity, Number(quantity) || 1))
    );
  }

  protected remove(productId: number): void {
    this.cart.remove(productId);
  }

  protected lineTotal(product: Product, quantity: number): number {
    return Number(product.discounted_price) * quantity;
  }

  protected isAvailable(product: Product): boolean {
    return product.quantity > 0 &&
      (!product.expiry_date || product.expiry_date >= this.today());
  }

  private today(): string {
    const now = new Date();
    return new Date(
      now.getTime() - now.getTimezoneOffset() * 60000
    ).toISOString().slice(0, 10);
  }
}
