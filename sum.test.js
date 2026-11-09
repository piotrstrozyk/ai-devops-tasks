const sum = require('../src/sum');

describe('Funkcja sum()', () => {
  test('powinna zwrócić sumę dwóch liczb', () => {
    expect(sum(2, 3)).toBe(5);
  });

  test('powinna poprawnie dodawać liczby ujemne', () => {
    expect(sum(-2, -3)).toBe(-5);
  });

  test('powinna zwrócić 0 dla dwóch zer', () => {
    expect(sum(0, 0)).toBe(0);
  });
});