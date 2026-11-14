import { Injectable, computed, effect, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { AuthService } from './auth';

export interface CartEntry {
  product_id: number;
  quantity: number;
}

export interface OrderItem {
  id: number;
  product: number | null;
  product_name: string;
  quantity: number;
  original_unit_price: string;
  unit_price: string;
  discount_percent: number;
  line_total: string;
}

export interface Order {
  id: number;
  status: string;
  total: string;
  created_at: string;
  items: OrderItem[];
}

@Injectable({ providedIn: 'root' })
export class ShoppingCartService {
  private readonly authService = inject(AuthService);
  private readonly storageKey = computed(
    () => `foodsaver_cart_${this.authService.getUser()?.id ?? 'guest'}`
  );

  readonly entries = signal<CartEntry[]>(this.readEntries());
  readonly itemCount = computed(
    () => this.entries().reduce((sum, item) => sum + item.quantity, 0)
  );

  constructor() {
    effect(() => {
      const userId = this.authService.currentUser()?.id;
      this.entries.set(this.readEntries(userId));
    });
  }

  add(productId: number, quantity: number): void {
    const current = this.entries();
    const existing = current.find(item => item.product_id === productId);
    this.persist(existing
      ? current.map(item => item.product_id === productId
        ? { ...item, quantity: item.quantity + quantity }
        : item)
      : [...current, { product_id: productId, quantity }]);
  }

  setQuantity(productId: number, quantity: number): void {
    if (quantity < 1) {
      this.remove(productId);
      return;
    }

    this.persist(this.entries().map(item => item.product_id === productId
      ? { ...item, quantity }
      : item));
  }

  remove(productId: number): void {
    this.persist(this.entries().filter(item => item.product_id !== productId));
  }

  clear(): void {
    this.persist([]);
  }

  private persist(entries: CartEntry[]): void {
    this.entries.set(entries);
    localStorage.setItem(this.storageKey(), JSON.stringify(entries));
  }

  private readEntries(userId = this.authService.getUser()?.id): CartEntry[] {
    if (!userId) return [];

    const key = `foodsaver_cart_${userId}`;
    const stored = localStorage.getItem(key);
    if (!stored) return [];

    try {
      const entries: unknown = JSON.parse(stored);
      if (!Array.isArray(entries)) throw new SyntaxError('Cart must be an array.');
      return entries.filter((entry): entry is CartEntry =>
        typeof entry?.product_id === 'number' &&
        Number.isInteger(entry.product_id) &&
        typeof entry?.quantity === 'number' &&
        Number.isInteger(entry.quantity) &&
        entry.quantity > 0
      );
    } catch (error) {
      if (!(error instanceof SyntaxError)) throw error;
      localStorage.removeItem(key);
      return [];
    }
  }
}

@Injectable({ providedIn: 'root' })
export class OrderService {
  private readonly http = inject(HttpClient);
  private readonly authService = inject(AuthService);
  private readonly apiUrl = 'http://127.0.0.1:8000/api/orders/';

  placeOrder(items: CartEntry[]): Observable<Order> {
    return this.http.post<Order>(
      this.apiUrl,
      { items },
      { headers: this.authService.authHeaders() }
    );
  }

  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(
      this.apiUrl,
      { headers: this.authService.authHeaders() }
    );
  }

  getOrder(id: number): Observable<Order> {
    return this.http.get<Order>(
      `${this.apiUrl}${id}/`,
      { headers: this.authService.authHeaders() }
    );
  }
}
