import { DecimalPipe } from '@angular/common';
import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { Product, ProductService } from '../../services/product';

@Component({
  selector: 'app-discover',
  standalone: true,
  imports: [DecimalPipe, FormsModule, RouterLink],
  templateUrl: './discover.html',
  styleUrl: './discover.css'
})
export class Discover implements OnInit {
  private readonly productService = inject(ProductService);
  private readonly route = inject(ActivatedRoute);

  protected readonly products = signal<Product[]>([]);
  protected readonly loading = signal(true);
  protected readonly error = signal('');
  protected readonly search = signal('');
  protected readonly categoryFilter = signal('All');
  protected readonly discountedOnly = signal(false);
  protected readonly minimumPrice = signal('');
  protected readonly maximumPrice = signal('');
  protected readonly sortOrder = signal('expiry');
  protected readonly isOffersPage =
    this.route.snapshot.routeConfig?.path === 'offers';

  protected readonly categories = computed(() => [
    'All',
    ...new Set(this.products().map(product => product.category))
  ]);

  protected readonly filteredProducts = computed(() => {
    const query = this.search().trim().toLowerCase();
    const minimum = this.minimumPrice() === ''
      ? null
      : Number(this.minimumPrice());
    const maximum = this.maximumPrice() === ''
      ? null
      : Number(this.maximumPrice());

    const filtered = this.products().filter(product => {
      const matchesQuery =
        !query ||
        product.name.toLowerCase().includes(query) ||
        product.category.toLowerCase().includes(query);
      const matchesCategory =
        this.categoryFilter() === 'All' ||
        product.category === this.categoryFilter();
      const matchesDiscount =
        (!this.discountedOnly() && !this.isOffersPage) ||
        product.discount_percent > 0;
      const price = Number(product.discounted_price);
      const matchesPrice =
        (minimum === null || price >= minimum) &&
        (maximum === null || price <= maximum);

      return matchesQuery && matchesCategory && matchesDiscount && matchesPrice;
    });

    return filtered.sort((first, second) => {
      if (this.sortOrder() === 'price-asc') {
        return Number(first.discounted_price) - Number(second.discounted_price);
      }
      if (this.sortOrder() === 'price-desc') {
        return Number(second.discounted_price) - Number(first.discounted_price);
      }
      if (this.sortOrder() === 'expiry') {
        if (!first.expiry_date) return second.expiry_date ? 1 : 0;
        if (!second.expiry_date) return -1;
        return first.expiry_date.localeCompare(second.expiry_date);
      }
      return first.expiry_date?.localeCompare(second.expiry_date ?? '') ?? 1;
    });
  });

  ngOnInit(): void {
    this.productService.getCatalog().subscribe({
      next: products => {
        this.products.set(products);
        this.loading.set(false);
      },
      error: error => {
        console.error('Catalog loading error:', error);
        this.error.set('Unable to load products.');
        this.loading.set(false);
      }
    });
  }

  protected getDiscount(product: Product): number {
    return product.discount_percent;
  }

  protected clearFilters(): void {
    this.search.set('');
    this.categoryFilter.set('All');
    this.discountedOnly.set(false);
    this.minimumPrice.set('');
    this.maximumPrice.set('');
    this.sortOrder.set('expiry');
  }
}
