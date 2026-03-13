
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  document.querySelectorAll(".twitch-embed").forEach((shell) => {
    const channel = shell.dataset.channel;
    if (!channel) return;
    const host = window.location.hostname || "localhost";
    if (host === "") return;
    const iframe = document.createElement("iframe");
    iframe.allowFullscreen = true;
    iframe.src = `https://player.twitch.tv/?channel=${encodeURIComponent(channel)}&parent=${encodeURIComponent(host)}`;
    iframe.title = `${channel} Twitch stream`;
    shell.innerHTML = "";
    shell.appendChild(iframe);
  });
});
