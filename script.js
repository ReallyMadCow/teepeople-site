for (const region of document.querySelectorAll("[data-player]")) {
  const trigger = region.querySelector("[data-load-player]");
  const slot = region.querySelector("[data-player-slot]");
  const externalLink = region.querySelector("a");
  const twitch = region.dataset.player === "twitch";
  const id = region.dataset.playerId;

  function playerFits() {
    return !twitch || (window.location.hostname && region.clientWidth >= 400);
  }

  function updateAvailability() {
    const fits = playerFits();
    const player = slot.querySelector("iframe");
    if (!fits && player) {
      const playerHadFocus = document.activeElement === player;
      player.remove();
      slot.hidden = true;
      if (playerHadFocus) externalLink.focus();
    }
    trigger.hidden = !fits || !slot.hidden;
  }

  trigger.addEventListener("click", () => {
    if (!playerFits() || !slot.hidden) return;

    const url = twitch
      ? new URL("https://player.twitch.tv/")
      : new URL(`https://www.youtube-nocookie.com/embed/${encodeURIComponent(id)}`);

    if (twitch) {
      url.searchParams.set("channel", id);
      url.searchParams.set("parent", window.location.hostname);
      url.searchParams.set("autoplay", "false");
    }

    const player = document.createElement("iframe");
    player.title = region.dataset.playerTitle;
    player.allowFullscreen = true;
    if (!twitch) player.allow = "encrypted-media; picture-in-picture";
    player.src = url.href;
    slot.appendChild(player);
    slot.hidden = false;
    trigger.hidden = true;
    player.focus();
  });

  updateAvailability();
  if (twitch) {
    if ("ResizeObserver" in window) {
      const observer = new ResizeObserver(updateAvailability);
      observer.observe(region);
    } else {
      window.addEventListener("resize", updateAvailability);
    }
  }
}
