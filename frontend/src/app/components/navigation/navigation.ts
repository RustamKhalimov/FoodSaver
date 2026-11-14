import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../services/auth';
import { ShoppingCartService } from '../../services/shopping';

@Component({
  selector: 'app-navigation',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navigation.html',
  styleUrl: './navigation.css'
})
export class Navigation {
  private readonly authService = inject(AuthService);
  private readonly cart = inject(ShoppingCartService);

  protected readonly isAdmin = this.authService.isAdmin;
  protected readonly cartItemCount = this.cart.itemCount;
}