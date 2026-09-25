// Put the CLIST rating (zerotrac's where CLIST has none) beside every
// link to a problem: after the title on a problem page, and after the
// Easy / Med. / Hard label in the rows of the problem lists (the row's
// title clips anything added to it). Icon links have no text and get none.
// ratings.json maps slug -> [clist, zerotrac]; `make mu-chrome` writes it.

const PROBLEM = /^\/problems\/([^/?#]+)\/?(?:description\/?)?$/;
const DIFFICULTY = new Set(["Easy", "Med.", "Medium", "Hard"]);

fetch(chrome.runtime.getURL("ratings.json"))
  .then((r) => r.json())
  .then((ratings) => {
    const label = (a) => {
      const m = PROBLEM.exec(new URL(a.href, location.href).pathname);
      const r = m && ratings[m[1]];
      if (!r || a.dataset.muRating || !a.textContent.trim()) return;
      const [clist, zerotrac] = r;
      const span = document.createElement("span");
      span.textContent = clist ? ` ${clist}` : ` ${zerotrac}`;
      span.title = clist ? `CLIST rating ${clist}` : `zerotrac rating ${zerotrac}`;
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
