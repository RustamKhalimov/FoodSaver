import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth';
import { environment } from '../../environments/environment';

export interface Product {
  id: number;
  name: string;
  barcode: string | null;
  image_url: string | null;
  category: string;
  expiry_date: string | null;
  quantity: number;
  regular_price: number;
  discount_percent: number;
  discounted_price: number;
  unit_size: string | null;
  created_at?: string;
  updated_at?: string;
}

export type ProductPayload = Omit<
  Product,
  'id' |
  'created_at' |
  'updated_at' |
  'discount_percent' |
  'discounted_price'
>;

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private readonly http = inject(HttpClient);
  private readonly authService = inject(AuthService);

  private readonly apiUrl = `${environment.apiUrl}/products/`;

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(this.apiUrl);
  }

  getCatalog(): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.apiUrl}catalog/`);
  }

  getProduct(id: number): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}${id}/`);
  }

  getExpiringProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(
      `${this.apiUrl}expiring/`
    );
  }

  addProduct(product: ProductPayload): Observable<Product> {
    return this.http.post<Product>(
      this.apiUrl,
      product,
      { headers: this.authService.authHeaders() }
    );
  }

  updateProduct(
    id: number,
    product: Partial<ProductPayload>
  ): Observable<Product> {
    return this.http.patch<Product>(
      `${this.apiUrl}${id}/`,
      product,
      { headers: this.authService.authHeaders() }
    );
  }

  deleteProduct(id: number): Observable<void> {
    return this.http.delete<void>(
      `${this.apiUrl}${id}/`,
      { headers: this.authService.authHeaders() }
    );
  }
}
