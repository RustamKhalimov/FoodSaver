import { ComponentFixture, TestBed } from '@angular/core/testing';
import { signal } from '@angular/core';
import { provideRouter } from '@angular/router';

import { AuthService } from '../../services/auth';
import { ShoppingCartService } from '../../services/shopping';
import { Navigation } from './navigation';

describe('Navigation', () => {
  let component: Navigation;
  let fixture: ComponentFixture<Navigation>;
  const adminRole = signal(false);

  beforeEach(async () => {
    adminRole.set(false);
    await TestBed.configureTestingModule({
      imports: [Navigation],
      providers: [
        provideRouter([]),
        {
          provide: AuthService,
          useValue: {
            isAdmin: adminRole,
            getUser: () => ({ id: 1 })
          }
        },
        {
          provide: ShoppingCartService,
          useValue: { itemCount: signal(0) }
        }
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(Navigation);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('shows shopping links without management links to customers', () => {
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Discover');
    expect(text).toContain('Account');
    expect(text).not.toContain('Inventory');
    expect(text).not.toContain('Rules');
  });

  it('shows management links to admins while retaining shopping links', () => {
    adminRole.set(true);
    fixture.detectChanges();

    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Inventory');
    expect(text).toContain('Rules');
    expect(text).toContain('Discover');
    expect(text).toContain('Account');
  });
});
