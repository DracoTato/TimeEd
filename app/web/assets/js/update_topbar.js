const topbarItems = document.querySelectorAll(".topbar ul li");
const activeBox = document.querySelector(".topbar ul .active-box");

const sections = Array.from(
    document.querySelectorAll("header, main section, footer")
);

const options = {
    rootMargin: "-49.5% 0px -49.5% 0px",
    threshold: 0,
};

const intersectionCallback = (entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            let elem = entry.target;
            const indx = sections.indexOf(elem);

            activeBox.style.left = `${topbarItems[indx].offsetLeft}px`;
            activeBox.style.width = `${topbarItems[indx].offsetWidth}px`;
        }
    });
};

const observer = new IntersectionObserver(intersectionCallback, options);

sections.forEach((section) => observer.observe(section));
