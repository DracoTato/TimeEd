const sidebar = document.querySelector(".sidebar");
const topbarBtn = document.querySelector(".topbar .topbar-icon");

const dataTable = document.querySelector(".data-table");
const tableSelectAll = document.querySelector(".data-table .select-all");
const tableDeleteAll = document.querySelector(".delete-all");

if (topbarBtn) {
  topbarBtn.addEventListener("click", () => {
    toggleSidebar();
  });
}

if (sidebar) {
  window.addEventListener("keydown", (e) => {
    const active = document.activeElement;
    const isTyping =
      active.tagName === "INPUT" ||
      active.tagName === "TEXTAREA" ||
      active.isContentEditable;

    if (!isTyping && e.key == "/") {
      e.preventDefault();
      toggleSidebar();
    }
  });
}

if (tableSelectAll) {
  tableSelectAll.addEventListener("change", (e) => {
    handleTablecheckbox(e);
  });
}

if (tableDeleteAll) {
  tableDeleteAll.addEventListener("click", (e) => {
    deleteSelected();
  });
}

function toggleSidebar() {
  sidebar.classList.toggle("visible");
}

function deleteGroup(url) {
  if (confirm("Are you sure you want to delete this group?")) {
    fetch(url, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => location.replace(data.url));
  }
}

function removeNotif(notif) {
  notif.classList.add("fade-out");
  notif.addEventListener("transitionend", () => {
    notif.remove();
  });
}
document.addEventListener("DOMContentLoaded", () => {
  const notifs = document.querySelectorAll(".notif-container .notif");
  const baseDelay = 12000;
  const step = 250;

  notifs.forEach((notif, index) => {
    const delay = baseDelay + index * step;

    setTimeout(() => {
      removeNotif(notif);
    }, delay);
  });
});

function handleTablecheckbox(e) {
  let checkboxes = dataTable
    .querySelector("tbody")
    .querySelectorAll("input[type='checkbox']");

  checkboxes.forEach((checkbox) => {
    checkbox.checked = e.target.checked;
  });
}

function getSelected() {
  if (dataTable) {
    return dataTable
      .querySelector("tbody")
      .querySelectorAll("input[type='checkbox']:checked");
  }
}

function deleteSelected() {
  const selected = getSelected();
  const data = [];

  for (let i = 0; i < selected.length; i++) {
    data.push({ id: selected[i].dataset.id, type: selected[i].dataset.type });
  }

  if (confirm(`Are you sure you want to delete ${data.length} items?`)) {
    fetch("/teacher/delete_all", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((result) => location.reload());
  }
}
