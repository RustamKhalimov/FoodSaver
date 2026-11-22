import { inject } from '@angular/core';
import {
  CanActivateFn,
  Router,
  Routes
} from '@angular/router';
import { catchError, map, of } from 'rxjs';

import { AuthService, UserRole } from './services/auth';

function roleDestination(role: UserRole): string {
  return role === 'admin' ? '/overview' : '/discover';
}

function authenticatedGuard(requiredRole?: UserRole): CanActivateFn {
  return () => {
    const authService = inject(AuthService);
    const router = inject(Router);

    if (!authService.isLoggedIn()) {
      return router.createUrlTree(['/login']);
    }

    return authService.getProfile().pipe(
      map(user => {
        if (requiredRole && user.role !== requiredRole) {
          return router.createUrlTree([roleDestination(user.role)]);
        }

        return true;
      }),
      catchError(() => {
        authService.removeToken();
        return of(router.createUrlTree(['/login']));
      })
    );
  };
}

const guestOnly: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (!authService.isLoggedIn()) {
    return true;
  }

  return authService.getProfile().pipe(
    map(user => router.createUrlTree([roleDestination(user.role)])),
    catchError(() => {
      authService.removeToken();
      return of(true);
    })
  );
};

const requireAuth = authenticatedGuard();
const requireAdmin = authenticatedGuard('admin');

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'overview',
    pathMatch: 'full'
  },
  {
    path: 'login',
    canActivate: [guestOnly],
    loadComponent: () =>
      import('./pages/login/login')
        .then(m => m.Login)
  },
  {
    path: 'register',
    canActivate: [guestOnly],
    loadComponent: () =>
      import('./pages/register/register')
        .then(m => m.Register)
  },
  {
    path: 'account',
    canActivate: [requireAuth],
    loadComponent: () =>
      import('./pages/account/account')
        .then(m => m.Account)
  },
  {
    path: 'discover',
    loadComponent: () =>
      import('./pages/discover/discover')
        .then(m => m.Discover)
  },
  {
    path: 'offers',
    loadComponent: () =>
      import('./pages/discover/discover')
        .then(m => m.Discover)
  },
  {
    path: 'product/:id',
    canActivate: [requireAuth],
    loadComponent: () =>
      import('./pages/product-detail/product-detail')
        .then(m => m.ProductDetail)
  },
  {
    path: 'cart',
    canActivate: [requireAuth],
    loadComponent: () =>
      import('./pages/cart/cart')
        .then(m => m.Cart)
  },
  {
    path: 'checkout',
    canActivate: [requireAuth],
    loadComponent: () =>
      import('./pages/checkout/checkout')
        .then(m => m.Checkout)
  },
  {
    path: 'orders',
    canActivate: [requireAuth],
    loadComponent: () =>
      import('./pages/orders/orders')
        .then(m => m.Orders)
  },
  {
    path: 'orders/:id',
    canActivate: [requireAuth],
    loadComponent: () =>
      import('./pages/orders/orders')
        .then(m => m.Orders)
  },
  {
    path: 'overview',
    canActivate: [requireAdmin],
    loadComponent: () =>
      import('./pages/overview/overview')
        .then(m => m.Overview)
  },
  {
    path: 'inventory',
    canActivate: [requireAdmin],
    loadComponent: () =>
      import('./pages/inventory/inventory')
        .then(m => m.Inventory)
  },
  {
    path: 'rules',
    canActivate: [requireAdmin],
    loadComponent: () =>
      import('./pages/rules/rules')
        .then(m => m.Rules)
  },
  {
    path: '**',
    redirectTo: 'overview'
  }
];
