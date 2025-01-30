let currentTabIndex = 0;

const form = document.querySelector("form");
const prev = document.querySelector("#prev");
const next = document.querySelector("#next");
const tabs = document.querySelectorAll(".tab");
const steps = document.querySelectorAll(".step-container span");

prev.addEventListener("click", (e) => {
    e.preventDefault(); // prevent form submission

    currentTabIndex = Math.max(currentTabIndex - 1, 0);
    showTab(tabs, currentTabIndex, prev, next, steps); // show the previous tab
});

next.addEventListener("click", (e) => {
    e.preventDefault(); // Prevent form submission

    if (validateTab(tabs[currentTabIndex])) {
        if (currentTabIndex == tabs.length - 1) {
            // check if this the last tab
            if (confirm("Are you sure you want to submit?")) {
                form.submit();
            }
        } else {
            steps[currentTabIndex].classList.add("finished"); // Mark the current step finishd
            currentTabIndex = Math.min(currentTabIndex + 1, tabs.length - 1);
            showTab(tabs, currentTabIndex, prev, next, steps); // show the next tab
        }
    }
});
if (![...tabs].some((tab) => tab.classList.contains("active"))) {
    showTab(tabs, currentTabIndex, prev, next, steps); // show the initial tab
}

/**
 * Show tab from tab list, this function is intended for forms divided into multiple tabs (steps).
 * it also updates the previous and next buttons if given.
 * @param {[Element]} tabsList List of tabs to iterate on.
 * @param {Number} tabIndex Tab index to show.
 * @param {HTMLButtonElement} prevBtn The previous tab button.
 * @param {HTMLButtonElement} nextBtn The next tab button.
 * @param {[Element]} tabIndicators A List of indicators w/ classList property,
 */
function showTab(tabsList, tabIndex, prevBtn, nextBtn, tabIndicators) {
    // Clamp the `tabIndex` between 0 and length of `tabsList`.
    tabIndex = Math.max(Math.min(tabIndex, tabsList.length - 1), 0);

    // Hide all tabs by default
    tabsList.forEach((tab) => {
        tab.classList.remove("active");
    });

    tabsList[tabIndex].classList.add("active");

    for (let i = 0; i < tabIndicators.length; i++) {
        tabIndicators[i].classList.remove("active");
    }
    tabIndicators[tabIndex].classList.add("active");

    if (tabIndex == 0) {
        prevBtn.style.display = "";
    } else {
        prevBtn.style.display = "block";
    }

    if (tabIndex == tabsList.length - 1) {
        nextBtn.innerHTML = "Submit";
        nextBtn.classList.add("submit");
    } else {
        nextBtn.innerHTML = "Next";
        nextBtn.classList.remove("submit");
    }
}

function validateTab(tab) {
    let valid = true;

    let inputs = tab.querySelectorAll("input:not(input[type='radio']");
    let radios = tab.querySelectorAll("input[type='radio']");

    let radioGroups = new Set();

    radios.forEach((radio) => {
        radioGroups.add(radio.getAttribute("name"));
    });

    // Check normal inputs
    inputs.forEach((input) => {
        const emailRegex = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/;

        if (input.value == "") {
            valid = false;
            markInvalid(input, "Please fill this field.");
        } else if (input.getAttribute("id") === "full_name") {
            if (input.value.trim().split(/\s/).length < 3) {
                valid = false;
                markInvalid(input, "Full name must be 3 names or more.");
            }
        } else if (input.type == "password") {
            if (input.getAttribute("autocomplete") === "current-password") {
                const passwordInput = document.querySelector(
                    "input[type='password']:not(input[autocomplete='current-password'])"
                );

                if (input.value !== passwordInput.value) {
                    valid = false;
                    markInvalid(input, "Passwords don't match.");
                }
            } else {
                if (input.value.length < 12 || input.value.length > 64) {
                    valid = false;
                    markInvalid(
                        input,
                        "Password must be more than 12 characters and less than 64 characters."
                    );
                } else if (new Set(input.value).size < 5) {
                    valid = false;
                    markInvalid(
                        input,
                        "Password must contain more than 5 unique characters."
                    );
                }
            }
        } else if (input.type == "email" && !input.value.match(emailRegex)) {
            valid = false;
            markInvalid(input, "Invalid email.");
        }
    });

    // Check radio button groups
    radioGroups.forEach((radioGroupName) => {
        const radioButtons = tab.querySelectorAll(
            `input[type='radio'][name='${radioGroupName}']`
        );

        const isRadioSelected = [...radioButtons].some(
            (radio) => radio.checked
        ); // check if any radios are checked

        if (!isRadioSelected) {
            valid = false;
            radioButtons.forEach((radioBtn) => {
                markInvalid(radioBtn, "Please fill this field.");
            });
        }
    });

    return valid;
}

/**
 * Adds invalid to the input classlist,
 * and adds an error message succeeding the element in hierarchy, all of this is cancelled upon input change.
 *
 * @param {HTMLInputElement} input
 * @param {string} error
 * @returns {null}
 * @example
 * markInvalid(document.querySelector("#invalidInput"))
 */
function markInvalid(input, error) {
    input.classList.add("invalid");

    if (input.type == "radio") {
        addError(
            input,
            error.replaceAll("this", "these").replaceAll("field", "fields")
        );
        input.addEventListener("change", () => {
            let [/** @type {Element} */ refElement, isGroup] =
                updateRefElement(input);

            if (isGroup) {
                for (let i = 0; i < refElement.children.length; i++) {
                    const child = refElement.children[i];
                    child.classList.remove("invalid");
                }
            } else {
                refElement.classList.remove("invalid");
            }

            if (
                refElement.nextElementSibling &&
                refElement.nextElementSibling.classList.contains("error")
            ) {
                refElement.nextElementSibling.remove();
            }
        });
    } else {
        addError(input, error);
        input.addEventListener("input", () => {
            input.classList.remove("invalid");
            if (
                input.nextElementSibling &&
                input.nextElementSibling.classList.contains("error")
            ) {
                input.nextElementSibling.remove();
            }
        });
    }
}

/**
 * Add a list after the given element with items corresponding to error,
 * supports appending errors, i.e. you can use multiple function calls on the same element without creating new lists.
 *
 * @param {Element} element
 * @param {string} error
 * @returns {null}
 * @example
 * addError(inputTag, "Please fill this field")
 */
function addError(element, error) {
    let errorContainer;
    let [refElement, _] = updateRefElement(element);

    // Some errors are bound to happen unintentially, so why not make it intential?
    // e.g. element is the last child, so nextSibling would be null
    try {
        if (refElement.nextElementSibling.classList.contains("error")) {
            errorContainer = refElement.nextElementSibling;
        } else {
            throw new Error(); // if next element isn't of class .errors
        }
    } catch (error) {
        errorContainer = document.createElement("p");
        errorContainer.classList.add("error");
        refElement.after(errorContainer);
    }

    errorContainer.innerHTML = String(error);
}

/**
 * Return the element parent if it's in an `input-group`, otherwise
 * return the element as is.
 *
 * @param {Element} element
 * @returns {[Element, boolean]} the reference element and a boolean that is equal to true if it's a group.
 */
function updateRefElement(element) {
    let refElement = element;

    if (element.parentElement.classList.contains("input-group")) {
        refElement = element.parentElement;
    }

    return [refElement, refElement !== element];
}
