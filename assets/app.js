const manifestUrl = "data/weeks/index.json";

const timeline = document.querySelector("#timeline");
const statusBox = document.querySelector("#status");
const areaFilter = document.querySelector("#area-filter");
const weekCount = document.querySelector("#week-count");
const areaCount = document.querySelector("#area-count");
const latestWeek = document.querySelector("#latest-week");

let weeks = [];

function titleCase(value) {
  return value
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function contributorNames(values) {
  const names = { gerrit: "Gerrit Renner", ricardo: "Ricardo Cunha" };
  return values.map((value) => names[value] ?? titleCase(value)).join(" · ");
}

function formatDateRange(start, end) {
  const formatter = new Intl.DateTimeFormat("en", {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC"
  });
  return `${formatter.format(new Date(`${start}T00:00:00Z`))} – ${formatter.format(new Date(`${end}T00:00:00Z`))}`;
}

function render(entries) {
  timeline.replaceChildren();

  if (entries.length === 0) {
    statusBox.hidden = false;
    statusBox.textContent = weeks.length === 0
      ? "The timeline is ready. The first reviewed weekly update will appear here."
      : "No timeline entries match the selected area.";
    return;
  }

  statusBox.hidden = true;
  for (const entry of entries) {
    const article = document.createElement("article");
    article.className = "timeline-entry";

    const label = document.createElement("div");
    label.className = "week-label";
    label.textContent = entry.week;

    const card = document.createElement("div");
    card.className = "entry-card";

    const dateText = document.createElement("p");
    dateText.className = "entry-date";
    dateText.textContent = formatDateRange(entry.start, entry.end);

    const summary = document.createElement("p");
    summary.className = "entry-summary";
    summary.textContent = entry.summary;

    const tags = document.createElement("div");
    tags.className = "tags";
    for (const area of entry.areas) {
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = titleCase(area);
      tags.append(tag);
    }

    const contributors = document.createElement("div");
    contributors.className = "contributors";
    contributors.textContent = `Contributors: ${contributorNames(entry.contributors)}`;

    card.append(dateText, summary, tags, contributors);
    article.append(label, card);
    timeline.append(article);
  }
}

function populateFilter(entries) {
  const areas = [...new Set(entries.flatMap((entry) => entry.areas))].sort();
  for (const area of areas) {
    const option = document.createElement("option");
    option.value = area;
    option.textContent = titleCase(area);
    areaFilter.append(option);
  }
  areaCount.textContent = String(areas.length);
}

async function loadTimeline() {
  try {
    const manifestResponse = await fetch(manifestUrl, { cache: "no-store" });
    if (!manifestResponse.ok) throw new Error(`Manifest request failed (${manifestResponse.status})`);
    const manifest = await manifestResponse.json();

    weeks = await Promise.all(
      manifest.weeks.map(async (weekId) => {
        const response = await fetch(`data/weeks/${weekId}.json`, { cache: "no-store" });
        if (!response.ok) throw new Error(`${weekId} request failed (${response.status})`);
        return response.json();
      })
    );

    weekCount.textContent = String(weeks.length);
    latestWeek.textContent = weeks[0]?.week ?? "—";
    populateFilter(weeks);
    render(weeks);
  } catch (error) {
    console.error(error);
    statusBox.hidden = false;
    statusBox.textContent = "The timeline data could not be loaded. Please try again later.";
  }
}

areaFilter.addEventListener("change", () => {
  const selected = areaFilter.value;
  render(selected === "all" ? weeks : weeks.filter((entry) => entry.areas.includes(selected)));
});

loadTimeline();
