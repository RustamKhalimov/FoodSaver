import { TestBed } from '@angular/core/testing';
import { signal } from '@angular/core';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';

import { App } from './app';
import { AuthService } from './services/auth';
import { BarcodeScannerService } from './services/barcode-scanner';
import { ProductService } from './services/product';

describe('App', () => {
  const authServiceMock = {
    isAuthenticated: signal(false),
    isAdmin: signal(false)
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [
        provideRouter([]),
        { provide: AuthService, useValue: authServiceMock },
        {
          provide: ProductService,
          useValue: {
            getProducts: () => of([]),
            getExpiringProducts: () => of([])
          }
        },
        { provide: BarcodeScannerService, useValue: {} }
      ],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should not render authenticated navigation before sign-in', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('app-navigation')).toBeNull();
  });
});
