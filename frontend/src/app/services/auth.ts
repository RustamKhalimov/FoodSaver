
import { computed, Injectable, signal } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

export type UserRole = 'admin' | 'customer';

export interface AuthUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
}

export interface AuthResponse {
  message: string;
  token: string;
  user: AuthUser;
  role?: UserRole;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly apiUrl = 'http://127.0.0.1:8000/api/accounts/';
  private readonly tokenKey = 'foodsaver_token';
  private readonly userKey = 'foodsaver_user';
  readonly currentUser = signal<AuthUser | null>(this.readStoredUser());
  private readonly profileVerified = signal(false);
  readonly isAdmin = computed(
    () => this.profileVerified() && this.currentUser()?.role === 'admin'
  );
  readonly isAuthenticated = computed(
    () => this.profileVerified() && this.currentUser() !== null &&
      !!this.getToken()
  );

  constructor(private http: HttpClient) {}

  register(data: {
    username: string;
    email: string;
    password: string;
  }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(
      `${this.apiUrl}register/`,
      data
    ).pipe(
      tap(response => this.persistSession(response))
    );
  }

  login(data: {
    email: string;
    password: string;
  }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(
      `${this.apiUrl}login/`,
      data
    ).pipe(
      tap(response => this.persistSession(response))
    );
  }

  getProfile(): Observable<AuthUser> {
    return this.http.get<AuthUser>(
      `${this.apiUrl}profile/`,
      { headers: this.authHeaders() }
    ).pipe(
      tap(user => {
        this.storeUser(user);
        this.profileVerified.set(true);
      })
    );
  }

  updateProfile(data: {
    email: string;
    first_name: string;
    last_name: string;
  }): Observable<AuthUser> {
    return this.http.patch<AuthUser>(
      `${this.apiUrl}profile/`,
      data,
      { headers: this.authHeaders() }
    );
  }

  changePassword(data: {
    old_password: string;
    new_password: string;
  }): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(
      `${this.apiUrl}change-password/`,
      data,
      { headers: this.authHeaders() }
    );
  }

  logout(): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(
      `${this.apiUrl}logout/`,
      {},
      { headers: this.authHeaders() }
    ).pipe(
      tap(() => this.removeToken())
    );
  }

  saveToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  persistSession(response: AuthResponse): void {
    this.saveToken(response.token);
    const user = {
      ...response.user,
      role: response.role ?? response.user?.role ?? 'customer'
    };

    this.storeUser(user);
    this.profileVerified.set(true);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  getUser(): AuthUser | null {
    return this.currentUser();
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  removeToken(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
    this.currentUser.set(null);
    this.profileVerified.set(false);
  }

  authHeaders(): HttpHeaders {
    return new HttpHeaders({
      Authorization: `Token ${this.getToken()}`
    });
  }

  private storeUser(user: AuthUser): void {
    this.currentUser.set(user);
    localStorage.setItem(this.userKey, JSON.stringify(user));
  }

  private readStoredUser(): AuthUser | null {
    const storedUser = localStorage.getItem(this.userKey);
    if (!storedUser) return null;

    try {
      return JSON.parse(storedUser) as AuthUser;
    } catch (error) {
      if (!(error instanceof SyntaxError)) throw error;
      localStorage.removeItem(this.userKey);
      return null;
    }
  }
}
