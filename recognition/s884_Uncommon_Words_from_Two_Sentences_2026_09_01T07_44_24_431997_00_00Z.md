A **sentence** is a string of single-space separated words where each word consists only of lowercase letters.

A word is **uncommon** if it appears exactly once in one of the sentences, and **does not appear** in the other sentence.

Given two **sentences** `s1` and `s2`, return \*a list of all the **uncommon words\***. You may return the answer in **any order**.

**Example 1:**

**Input:** s1 = "this apple is sweet", s2 = "this apple is sour"

**Output:** ["sweet","sour"]

**Explanation:**

The word `"sweet"` appears only in `s1`, while the word `"sour"` appears only in `s2`.

**Example 2:**

**Input:** s1 = "apple apple", s2 = "banana"

**Output:** ["banana"]

**Constraints:**

- `1 <= s1.length, s2.length <= 200`
- `s1` and `s2` consist of lowercase English letters and spaces.
- `s1` and `s2` do not have leading or trailing spaces.
- All the words in `s1` and `s2` are separated by a single space.

## <!-- answer -->

The simpliest solution here is to build two sets, s1s which holds each word in s1, and s2s which holds every word in s2 (easy enough to split the strings in python with .split()).

Then one can simply take the intersection of both sets with s1s ^ s2s. That is the solution.

Ah no, nevermind that:

"A word is **uncommon** if it appears exactly once in one of the sentences, and **does not appear** in the other sentence."

This means sets are out. Then we need a counter.

s1 = "apple apple"
s2 = "banana"

```
c1 = {
    'apple': 2,
}

c2 = {
    'banana': 1,
}
```

Now we only need to focus on words that appear once. So we can simply add the counters to one another, or in fact take one big counter of both sentences would also work, and only return words that appear once. e.g:

```
c1 = {
    'this': 1,
    'apple': 1,
    'is': 1:
    'sweet': 1
}


c2 = {
    'this': 1,
    'apple': 1,
    'is': 1:
    'sour': 1
}


becomes:

c = {
    'this': 2,
    'apple': 2,
    'is': 2,
    'sweet': 1,
    'sour': 1
}

Filtering for one:

c = {
    'sweet': 1,
    'sour': 1
}

Or:

sweet, sour


```

<!-- spot {"problem": "884", "target": "counter-build", "reason": "untested, 198 reachable through it", "seconds": 596} -->
