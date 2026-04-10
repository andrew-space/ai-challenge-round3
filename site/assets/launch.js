(() => {
  const API_URL = "https://fdo.rocketlaunch.live/json/launches/next/20";
  const REFRESH_INTERVAL_MS = 5 * 60 * 1000;

  const dom = {
    status: document.getElementById("apiStatus"),
    nextMission: document.getElementById("nextMission"),
    nextDetails: document.getElementById("nextDetails"),
    countdown: document.getElementById("countdown"),
    tableBody: document.getElementById("launchTableBody"),
    refreshBtn: document.getElementById("refreshBtn")
  };

  let launches = [];
  let nextLaunchDate = null;
  let countdownTimer = null;

  function setStatus(text, mode) {
    dom.status.textContent = text;
    dom.status.classList.remove("ok", "error");
    if (mode) {
      dom.status.classList.add(mode);
    }
  }

  function parseLaunch(item) {
    const mission = item.name || "Unknown mission";
    const rocket = item.vehicle?.name || item.provider?.name || "Unknown rocket";
    const site = item.pad?.location?.name || item.pad?.name || "Unknown launch site";

    let launchDate = null;
    if (item.sort_date) {
      launchDate = new Date(Number(item.sort_date) * 1000);
    } else if (item.win_open) {
      launchDate = new Date(item.win_open);
    }

    return {
      mission,
      rocket,
      site,
      launchDate,
      launchLabel: launchDate && !Number.isNaN(launchDate.getTime())
        ? launchDate.toISOString().replace("T", " ").slice(0, 16) + " UTC"
        : "TBD"
    };
  }

  function renderTable(items) {
    if (!items.length) {
      dom.tableBody.innerHTML = '<tr><td colspan="4" class="error-row">No upcoming launches available right now.</td></tr>';
      return;
    }

    dom.tableBody.innerHTML = items.map((launch) => `
      <tr>
        <td>${escapeHtml(launch.mission)}</td>
        <td>${escapeHtml(launch.rocket)}</td>
        <td>${escapeHtml(launch.site)}</td>
        <td>${escapeHtml(launch.launchLabel)}</td>
      </tr>
    `).join("");
  }

  function renderNextLaunch(launch) {
    if (!launch) {
      dom.nextMission.textContent = "No launch data";
      dom.nextDetails.textContent = "Feed did not return upcoming events.";
      dom.countdown.textContent = "--:--:--:--";
      nextLaunchDate = null;
      return;
    }

    dom.nextMission.textContent = launch.mission;
    dom.nextDetails.textContent = `${launch.rocket} • ${launch.site} • ${launch.launchLabel}`;
    nextLaunchDate = launch.launchDate;
    updateCountdown();
  }

  function updateCountdown() {
    if (!nextLaunchDate || Number.isNaN(nextLaunchDate.getTime())) {
      dom.countdown.textContent = "TBD";
      return;
    }

    const now = new Date();
    const diff = nextLaunchDate.getTime() - now.getTime();

    if (diff <= 0) {
      dom.countdown.textContent = "LIFTOFF WINDOW";
      return;
    }

    const totalSeconds = Math.floor(diff / 1000);
    const days = Math.floor(totalSeconds / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    dom.countdown.textContent = `${pad(days)}:${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
  }

  function pad(value) {
    return String(value).padStart(2, "0");
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  async function loadLaunches() {
    setStatus("Refreshing live data...", null);

    try {
      const response = await fetch(API_URL, {
        method: "GET",
        headers: {
          Accept: "application/json"
        }
      });

      if (!response.ok) {
        throw new Error(`API error ${response.status}`);
      }

      const payload = await response.json();
      launches = Array.isArray(payload.result) ? payload.result.map(parseLaunch) : [];
      launches.sort((a, b) => {
        if (!a.launchDate) return 1;
        if (!b.launchDate) return -1;
        return a.launchDate.getTime() - b.launchDate.getTime();
      });

      renderTable(launches);
      renderNextLaunch(launches[0]);
      setStatus(`Live feed active • ${launches.length} launches loaded`, "ok");
    } catch (error) {
      renderTable([]);
      renderNextLaunch(null);
      setStatus("Live feed unavailable (retrying automatically)", "error");
      console.error("Launch data error", error);
    }
  }

  function bootstrap() {
    dom.refreshBtn.addEventListener("click", loadLaunches);
    loadLaunches();

    countdownTimer = window.setInterval(updateCountdown, 1000);
    window.setInterval(loadLaunches, REFRESH_INTERVAL_MS);

    window.addEventListener("beforeunload", () => {
      if (countdownTimer) {
        window.clearInterval(countdownTimer);
      }
    });
  }

  bootstrap();
})();
