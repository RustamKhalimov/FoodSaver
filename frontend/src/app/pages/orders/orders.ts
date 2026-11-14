import { DatePipe, DecimalPipe } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { Order, OrderService } from '../../services/shopping';

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [DatePipe, DecimalPipe, RouterLink],
  templateUrl: './orders.html',
  styleUrl: './orders.css'
})
export class Orders implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly orderService = inject(OrderService);

  protected readonly orders = signal<Order[]>([]);
  protected readonly selectedOrder = signal<Order | null>(null);
  protected readonly loading = signal(true);
  protected readonly error = signal('');
  protected readonly confirmed = signal(false);

  ngOnInit(): void {
    this.confirmed.set(
      this.route.snapshot.queryParamMap.get('confirmed') === '1'
    );
    const id = Number(this.route.snapshot.paramMap.get('id'));

    if (Number.isInteger(id) && id > 0) {
      this.orderService.getOrder(id).subscribe({
        next: order => {
          this.selectedOrder.set(order);
          this.loading.set(false);
        },
        error: error => {
          console.error('Order loading error:', error);
          this.error.set('Unable to load this order.');
          this.loading.set(false);
        }
      });
      return;
    }

    this.orderService.getOrders().subscribe({
      next: orders => {
        this.orders.set(orders);
        this.loading.set(false);
      },
      error: error => {
        console.error('Order history loading error:', error);
        this.error.set('Unable to load your orders.');
        this.loading.set(false);
      }
    });
  }
}
