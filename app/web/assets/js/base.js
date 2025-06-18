const sidebar = document.querySelector(".sidebar");
const topbarBtn = document.querySelector(".topbar .topbar-icon");

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

function toggleSidebar() {
  sidebar.classList.toggle("visible");
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
