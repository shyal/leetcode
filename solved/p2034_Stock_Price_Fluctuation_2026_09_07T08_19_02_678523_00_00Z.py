"""
URL: https://leetcode.com/problems/stock-price-fluctuation/description/?envType=problem-list-v2&envId=vn57k9wr

2034. Stock Price Fluctuation

You are given a stream of records about a particular stock. Each record contains a timestamp and the corresponding price of the stock at that timestamp.

Unfortunately due to the volatile nature of the stock market, the records do not come in order. Even worse, some records may be incorrect. Another record with the same timestamp may appear later in the stream correcting the price of the previous wrong record.

Design an algorithm that:

- Updates the price of the stock at a particular timestamp, correcting the price from any previous records at the timestamp.
- Finds the latest price of the stock based on the current records. The latest price is the price at the latest timestamp recorded.
- Finds the maximum price the stock has been based on the current records.
- Finds the minimum price the stock has been based on the current records.

Implement the StockPrice class:

- StockPrice() Initializes the object with no price records.
- void update(int timestamp, int price) Updates the price of the stock at the given timestamp.
- int current() Returns the latest price of the stock.
- int maximum() Returns the maximum price of the stock.
- int minimum() Returns the minimum price of the stock.

Example 1:

Input
["StockPrice","update","update","current","maximum","update","maximum","update","minimum"]
[[],[1,10],[2,5],[],[],[1,3],[],[4,2],[]]
Output
[null, null, null, 5, 10, null, 5, null, 2]

Explanation
StockPrice stockPrice = new StockPrice();
stockPrice.update(1, 10); // Timestamps are [1] with corresponding prices [10].
stockPrice.update(2, 5);  // Timestamps are [1,2] with corresponding prices [10,5].
stockPrice.current();     // return 5, the latest timestamp is 2 with the price being 5.
stockPrice.maximum();     // return 10, the maximum price is 10 at timestamp 1.
stockPrice.update(1, 3);  // The previous timestamp 1 had the wrong price, so it is updated to 3.
                          // Timestamps are [1,2] with corresponding prices [3,5].
stockPrice.maximum();     // return 5, the maximum price is 5 after the correction.
stockPrice.update(4, 2);  // Timestamps are [1,2,4] with corresponding prices [3,5,2].
stockPrice.minimum();     // return 2, the minimum price is 2 at timestamp 4.

Constraints:

    1 <= timestamp, price <= 10^9
    At most 10^5 calls will be made in total to update, current, maximum, and minimum.
    current, maximum, and minimum will be called only after update has been called at least once.

---


I kept being wobbly at these questions, so discussed broadly before trying this questions a couple of times.
So could be considered hinted.


"""


class StockPrice:

    def __init__(self):
        self.timestamps = []
        self.min_prices = []
        self.max_prices = []
        self.prices = {}

    def update(self, timestamp: int, price: int) -> None:
        self.prices[-timestamp] = price
        heappush(self.timestamps, -timestamp)
        heappush(self.min_prices, (price, timestamp))
        heappush(self.max_prices, (-price, timestamp))

    def current(self) -> int:
        ts = self.timestamps[0]
        return self.prices[ts]

    def maximum(self) -> int:
        while True:
            price, ts = heappop(self.max_prices)
            if self.prices[-ts] == -price:
                return -price

    def minimum(self) -> int:
        while True:
            price, ts = heappop(self.min_prices)
            if self.prices[-ts] == price:
                return price


sol = StockPrice()

sol.update(1, 10)
sol.update(2, 5)
print(sol.current())  # 5
assert sol.current() == 5
assert sol.maximum() == 10
sol.update(1, 3)
assert sol.maximum() == 5
sol.update(4, 2)
assert sol.minimum() == 2


# edge cases: one line each, the values are the reference solution's.
assert [(sp := StockPrice()), sp.update(1, 1), sp.current()][
    -1
] == 1  # single_record_smallest_legal_values
assert [(sp := StockPrice()), sp.update(10**9, 10**9), sp.maximum()][
    -1
] == 1000000000  # single_record_largest_legal_values
assert [(sp := StockPrice()), sp.update(5, 7), sp.update(5, 7), sp.minimum()][
    -1
] == 7  # same_timestamp_updated_to_identical_price
assert [(sp := StockPrice()), sp.update(3, 8), sp.update(3, 2), sp.maximum()][
    -1
] == 2  # only_timestamp_corrected_downward
assert [(sp := StockPrice()), sp.update(3, 8), sp.update(3, 2), sp.current()][
    -1
] == 2  # latest_timestamp_price_corrected
assert [(sp := StockPrice()), sp.update(2, 4), sp.update(1, 9), sp.current()][
    -1
] == 4  # records_arrive_out_of_order
assert [
    (sp := StockPrice()),
    sp.update(1, 5),
    sp.update(2, 5),
    sp.update(3, 5),
    (sp.maximum(), sp.minimum()),
][-1] == (
    5,
    5,
)  # all_records_share_one_price
assert [
    (sp := StockPrice()),
    sp.update(1, 2),
    sp.update(2, 9),
    sp.update(1, 100),
    (sp.maximum(), sp.current()),
][-1] == (
    100,
    9,
)  # earlier_timestamp_corrected_above_all
assert [
    (sp := StockPrice()),
    sp.update(4, 6),
    sp.update(4, 1),
    sp.update(4, 9),
    (sp.minimum(), sp.maximum(), sp.current()),
][-1] == (
    9,
    9,
    9,
)  # one_timestamp_corrected_repeatedly
assert [
    (sp := StockPrice()),
    sp.update(1, 10),
    sp.update(2, 5),
    sp.update(1, 3),
    sp.update(4, 2),
    (sp.current(), sp.maximum(), sp.minimum()),
][-1] == (
    2,
    5,
    2,
)  # mixed_updates_then_all_queries
assert [
    (sp := StockPrice()),
    [sp.update(t, 100 - t) for t in range(1, 51)],
    (sp.current(), sp.maximum(), sp.minimum()),
][-1] == (
    50,
    99,
    50,
)  # fifty_records_prices_decreasing_with_time
assert [
    (sp := StockPrice()),
    [sp.update(t, t) for t in range(1, 31)],
    [sp.update(t, 50 - t) for t in range(1, 31)],
    (sp.current(), sp.maximum(), sp.minimum()),
][-1] == (
    20,
    49,
    20,
)  # every_record_corrected_in_a_second_pass
