import { describe, expect, it } from 'vitest';
import { expirationStatus } from './expiration-status';

describe('expirationStatus', () => {
  const today = new Date(2026, 10, 21);

  it('classifies twenty dates across past, urgent, soon, and fresh periods', () => {
    const statuses = Array.from({ length: 20 }, (_, index) => {
      const offset = index - 10;
      const date = new Date(2026, 10, 21 + offset);
      const isoDate = [
        date.getFullYear(),
        String(date.getMonth() + 1).padStart(2, '0'),
        String(date.getDate()).padStart(2, '0')
      ].join('-');
      return expirationStatus(isoDate, today);
    });

    expect(statuses.slice(0, 10)).toEqual(Array(10).fill('expired'));
    expect(statuses.slice(10, 12)).toEqual(['urgent', 'urgent']);
    expect(statuses.slice(12, 14)).toEqual(['expiring-soon', 'expiring-soon']);
    expect(statuses.slice(14)).toEqual(Array(6).fill('fresh'));
  });

  it('treats a product expiring today as urgent and handles missing dates', () => {
    expect(expirationStatus('2026-11-21', today)).toBe('urgent');
    expect(expirationStatus(null, today)).toBe('no-expiry');
  });
});
