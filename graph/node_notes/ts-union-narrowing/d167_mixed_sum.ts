function mixedSum(values: (number | string)[]): number {
  let total = 0;
  for (const v of values) {
    total += typeof v === "string" ? Number(v) : v;
  }
  return total;
}
