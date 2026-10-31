// Put the problem's rating beside every link to it: after the title on a
// problem page, and after the Easy / Med. / Hard label in the rows of the
// problem lists (the row's title clips anything added to it). Icon links
// have no text and get none. ratings.json maps slug -> rating, the one
// number the repo shows for a problem (make next, the README); `make
// mu-chrome` writes it from kg::model::combined_ratings.

const PROBLEM = /^\/problems\/([^/?#]+)\/?(?:description\/?)?$/;
const DIFFICULTY = new Set(["Easy", "Med.", "Medium", "Hard"]);

fetch(chrome.runtime.getURL("ratings.json"))
  .then((r) => r.json())
  .then((ratings) => {
    const label = (a) => {
      const m = PROBLEM.exec(new URL(a.href, location.href).pathname);
      const rating = m && ratings[m[1]];
      if (!rating || a.dataset.muRating || !a.textContent.trim()) return;
      const span = document.createElement("span");
      span.textContent = ` ${rating}`;
      span.title = `rating ${rating}`;
      span.style.cssText = "margin-left:6px;font-size:12px;font-weight:600;color:#e8a33d;";
      a.dataset.muRating = "1";
      const leaves = [...a.querySelectorAll("*")].filter((e) => !e.children.length);
      const level = leaves.find((e) => DIFFICULTY.has(e.textContent.trim()));
      if (level) level.after(span);
      else if (!a.children.length) a.append(span);
    };
    const scan = () => document.querySelectorAll('a[href*="/problems/"]').forEach(label);
    scan();
    let queued = false;
    new MutationObserver(() => {
      if (queued) return;
      queued = true;
      requestAnimationFrame(() => {
        queued = false;
        scan();
      });
    }).observe(document.body, { childList: true, subtree: true });
  });
