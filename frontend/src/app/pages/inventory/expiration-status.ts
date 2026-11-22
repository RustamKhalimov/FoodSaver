export type ExpirationStatus =
  | 'expired'
  | 'urgent'
  | 'expiring-soon'
  | 'fresh'
  | 'no-expiry';

const DAY_MS = 24 * 60 * 60 * 1000;

function calendarDay(date: Date): number {
  return Math.floor(Date.UTC(
    date.getFullYear(),
    date.getMonth(),
    date.getDate()
  ) / DAY_MS);
}

export function daysUntilExpiry(expiryDate: string, today = new Date()): number {
  const [year, month, day] = expiryDate.split('-').map(Number);
  const expiryDay = Math.floor(Date.UTC(year, month - 1, day) / DAY_MS);
  return expiryDay - calendarDay(today);
}

export function expirationStatus(
  expiryDate: string | null,
  today = new Date()
): ExpirationStatus {
  if (!expiryDate) return 'no-expiry';

  const days = daysUntilExpiry(expiryDate, today);
  if (days < 0) return 'expired';
  if (days <= 1) return 'urgent';
  if (days <= 3) return 'expiring-soon';
  return 'fresh';
}

export function expirationLabel(
  expiryDate: string | null,
  today = new Date()
): string {
  const status = expirationStatus(expiryDate, today);
  if (status === 'no-expiry') return 'No expiry date';
  if (status === 'expired') return 'Expired';

  const days = daysUntilExpiry(expiryDate!, today);
  if (status === 'urgent') {
    return days === 0 ? 'Urgent · Expires today' : 'Urgent · 1 day left';
  }
  if (status === 'expiring-soon') {
    return `Expiring soon · ${days} days left`;
  }
  return `Fresh · ${days} days left`;
}
