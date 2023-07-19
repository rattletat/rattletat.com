function splitURL(url) {
  const urlObject = new URL(url);
  const pathParts = urlObject.pathname.split("/").filter((part) => part);

  return {
    host: urlObject.hostname,
    user: pathParts[0],
    id: pathParts[1],
  };
}

function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

var commentsLoaded = false;

function toot_active(toot, what) {
  var count = toot[what + "_count"];
  return count > 0 ? "active" : "";
}

function toot_count(toot, what) {
  var count = toot[what + "_count"];
  return count > 0 ? count : "";
}

function user_account(account) {
  var result = `@${account.acct}`;
  if (account.acct.indexOf("@") === -1) {
    var domain = new URL(account.url);
    result += `@${domain.hostname}`;
  }
  return result;
}

function render_toots(toots, in_reply_to, depth) {
  var tootsToRender = toots
    .filter((toot) => toot.in_reply_to_id === in_reply_to)
    .sort((a, b) => a.created_at.localeCompare(b.created_at));
  tootsToRender.forEach((toot) => render_toot(toots, toot, depth));
}

function render_toot(toots, toot, depth) {
  toot.account.display_name = escapeHtml(toot.account.display_name);
  toot.account.emojis.forEach((emoji) => {
    toot.account.display_name = toot.account.display_name.replace(
      `:${emoji.shortcode}:`,
      `<img src="${escapeHtml(emoji.static_url)}" alt="Emoji ${
        emoji.shortcode
      }" height="20" width="20" />`
    );
  });
  mastodonComment = `<div class="mastodon-comment" style="margin-left: calc(var(--mastodon-comment-indent) * ${depth})">
        <div class="author">
          <div class="avatar">
            <img src="${escapeHtml(
              toot.account.avatar_static
            )}" height=60 width=60 alt="">
          </div>
          <div class="details">
            <a class="name" href="${toot.account.url}" rel="nofollow">${
    toot.account.display_name
  }</a>
            <a class="user" href="${
              toot.account.url
            }" rel="nofollow">${user_account(toot.account)}</a>
          </div>
          <a class="date" href="${
            toot.url
          }" rel="nofollow">${toot.created_at.substr(
    0,
    10
  )} ${toot.created_at.substr(11, 8)}</a>
        </div>
        <div class="content">${toot.content}</div>
        <div class="attachments">
          ${toot.media_attachments
            .map((attachment) => {
              if (attachment.type === "image") {
                return `<a href="${attachment.url}" rel="nofollow"><img src="${attachment.preview_url}" alt="${attachment.description}" /></a>`;
              } else if (attachment.type === "video") {
                return `<video controls><source src="${attachment.url}" type="${attachment.mime_type}"></video>`;
              } else if (attachment.type === "gifv") {
                return `<video autoplay loop muted playsinline><source src="${attachment.url}" type="${attachment.mime_type}"></video>`;
              } else if (attachment.type === "audio") {
                return `<audio controls><source src="${attachment.url}" type="${attachment.mime_type}"></audio>`;
              } else {
                return `<a href="${attachment.url}" rel="nofollow">${attachment.type}</a>`;
              }
            })
            .join("")}
        </div>
        <div class="status">
        ${
          toot["replies_count"]
            ? `<div class="replies"> <a href="${toot.url}" rel="nofollow">` +
              toot["replies_count"] +
              (toot["replies_count"] == 1 ? " reply" : " replies") +
              `</a></div>`
            : ""
        }
        ${
          toot["reblogs_count"]
            ? `<div class="reblogs"> <a href="${toot.url}" rel="nofollow">` +
              toot["reblogs_count"] +
              (toot["reblogs_count"] == 1 ? " boost" : " boosts") +
              `</a></div>`
            : ""
        }
        ${
          toot["favourites_count"]
            ? `<div class="favourites"> <a href="${toot.url}" rel="nofollow">` +
              toot["favourites_count"] +
              (toot["favourites_count"] == 1 ? " like" : " likes") +
              `</a></div>`
            : ""
        }
        </div>
      </div>`;
  document
    .getElementById("mastodon-comments-list")
    .appendChild(
      DOMPurify.sanitize(mastodonComment, { RETURN_DOM_FRAGMENT: true })
    );

  render_toots(toots, toot.id, depth + 1);
}

function loadComments() {
  if (commentsLoaded) return;

  document.getElementById("mastodon-comments-list").innerHTML =
    "Loading comments from the Fediverse...";

  fetch("https://" + host + "/api/v1/statuses/" + id + "/context")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (
        data["descendants"] &&
        Array.isArray(data["descendants"]) &&
        data["descendants"].length > 0
      ) {
        document.getElementById("mastodon-comments-list").innerHTML = "";
        render_toots(data["descendants"], id, 0);
      } else {
        document.getElementById("mastodon-comments-list").innerHTML =
          "<p>No comments found</p>";
      }

      commentsLoaded = true;
    });
}

function respondToVisibility(element, callback) {
  var options = {
    root: null,
  };

  var observer = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.intersectionRatio > 0) {
        callback();
      }
    });
  }, options);

  observer.observe(element);
}

var comments = document.getElementById("mastodon-comments-list");
respondToVisibility(comments, loadComments);
