import { DecimalPipe } from '@angular/common';
import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { Product, ProductService } from '../../services/product';
import { ShoppingCartService } from '../../services/shopping';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [DecimalPipe, RouterLink],
  templateUrl: './product-detail.html',
  styleUrl: './product-detail.css'
})
export class ProductDetail implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly productService = inject(ProductService);
  private readonly cart = inject(ShoppingCartService);

  protected readonly product = signal<Product | null>(null);
  protected readonly quantity = signal(1);
  protected readonly loading = signal(true);
  protected readonly error = signal('');
  protected readonly success = signal('');
  protected readonly unavailable = computed(() => {
    const product = this.product();
    return !product ||
      product.quantity < 1 ||
      (!!product.expiry_date && product.expiry_date < this.today());
  });

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!Number.isInteger(id) || id < 1) {
      this.error.set('Invalid product.');
      this.loading.set(false);
      return;
    }

    this.productService.getProduct(id).subscribe({
      next: product => {
        this.product.set(product);
        this.loading.set(false);
      },
      error: error => {
        console.error('Product detail loading error:', error);
        this.error.set('Unable to load this product.');
        this.loading.set(false);
      }
    });
  }

  protected changeQuantity(value: number): void {
    const product = this.product();
    if (!product) return;
    this.quantity.set(Math.max(1, Math.min(product.quantity, Number(value) || 1)));
    this.success.set('');
  }

  protected addToCart(): void {
    const product = this.product();
    if (!product || this.unavailable()) {
      this.error.set('This product is no longer available.');
      return;
    }
    if (this.quantity() > product.quantity) {
      this.error.set('The selected quantity exceeds available stock.');
      return;
    }
    this.cart.add(product.id, this.quantity());
    this.error.set('');
    this.success.set('Added to your shopping cart.');
  }

  private today(): string {
    const now = new Date();
    const localDate = new Date(
      now.getTime() - now.getTimezoneOffset() * 60000
    );
    return localDate.toISOString().slice(0, 10);
  }
}
