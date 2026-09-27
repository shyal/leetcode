// DRILL: Order Total
// TRAINS: ts-object-type
//
// Given an array `items`, each an object with a `name`, a `price` and an
// optional `qty`, return the sum of price times qty. A missing qty counts as
// 1; a qty of 0 counts as 0.
//
// Example 1:
//
// Input: items = [{ name: "pen", price: 2, qty: 3 }, { name: "pad", price: 5 }]
// Output: 11
//
// Example 2:
//
// Input: items = []
// Output: 0
//
// Example 3:
//
// Input: items = [{ name: "cup", price: 4, qty: 0 }]
// Output: 0
//
// Constraints:
//
//     0 <= items.length <= 10^4
//     0 <= price, qty <= 10^6
//
//     REQUIRED: O(n); the parameter is typed with a declared type or
//     interface in which qty is optional; a missing qty is 1 and a qty of 0
//     stays 0. NO any, NO ||.

import assert from "node:assert/strict";

type Item = { name: string; price: number; qty?: number };

function orderTotal(items: Item[]): number {
  let total: number = 0;
  for (const item of items) {
    total += item.price * (item.qty ?? 1);
  }
  return total;
}

console.log(
  orderTotal([
    { name: "pen", price: 2, qty: 3 },
    { name: "pad", price: 5 },
  ]),
);

assert.deepEqual(
  orderTotal([
    { name: "pen", price: 2, qty: 3 },
    { name: "pad", price: 5 },
  ]),
  11,
);
assert.deepEqual(orderTotal([]), 0);
assert.deepEqual(orderTotal([{ name: "cup", price: 4, qty: 0 }]), 0);
assert.deepEqual(
  orderTotal([
    { name: "ink", price: 3 },
    { name: "clip", price: 1, qty: 10 },
    { name: "tape", price: 2 },
  ]),
  15,
);
