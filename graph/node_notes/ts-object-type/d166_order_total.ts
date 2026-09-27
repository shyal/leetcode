type Item = {
  name: string;
  price: number;
  qty?: number;
};

function orderTotal(items: Item[]): number {
  let total = 0;
  for (const item of items) total += item.price * (item.qty ?? 1);
  return total;
}
