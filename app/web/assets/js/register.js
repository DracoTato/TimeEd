const form = document.querySelector("form");
const inputs = form.querySelectorAll(".input input");

const inputContainers = form.querySelectorAll(".inputs-container > div");

form.addEventListener("submit", (e) => {
    e.preventDefault();
    validateForm();
});

inputContainers.forEach((container) => {
    let input = container.querySelector("input");
    let label = container.querySelector(":scope > label");

    if (input && label && input.required) {
        if (!label.innerText.includes("*")) {
            label.innerText += "*";
        }
    }
});

inputs.forEach((input) => {
    input.addEventListener("input", (e) => {
        validateInput(input);
    });
});

/**
 *
 * @param {HTMLElement} element
 * @param {String} target
 */
function getParentUntil(element, target) {
    parent = element.parentElement;

    while (parent && !parent.matches(target)) {
        parent = parent.parentElement;
    }
    return parent;
}

/**
 *
 * @param {HTMLInputElement} input
 */
function getErrorList(input) {
    const parent = getParentUntil(input, ".inputs-container > div");
    return parent.querySelector("ul.errors");
}

/**
 *
 * @param {HTMLInputElement} input
 */
function markInvalid(input, error = null) {
    input.classList.remove("valid");
    input.classList.add("invalid");

    const errorList = getErrorList(input);

    if (error && !errorList.innerHTML.includes(error)) {
        errorList.innerHTML = "";
        let li = document.createElement("li");
        li.innerText = error;
        errorList.appendChild(li);
    }
}

/**
 *
 * @param {HTMLInputElement} input
 */
function markValid(input) {
    input.classList.remove("invalid");
    input.classList.add("valid");

    const errorList = getErrorList(input);
    if (errorList.children) {
        errorList.innerHTML = "";
    }
}

const customValidators = {
    confirm_password: (input) => {
        if (input.value == form.querySelector("input#password").value) {
            markValid(input);
            return true;
        } else {
            markInvalid(input, "Passwords don't match.");
            return false;
        }
    },
    full_name: (input) => {
        const nameLen = input.value.trim().split(" ").length;
        if (nameLen >= 2 && nameLen <= 5) {
            markValid(input);
            return true;
        } else {
            markInvalid(input, "Full name must be 2-5 names.");
            return false;
        }
    },
    email: (input) => {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (emailRegex.test(input.value)) {
            markValid(input);
            return true;
        } else {
            markInvalid(input, "Invalid email address.");
            return false;
        }
    },
    password: (input) => {
        if (new Set(input.value).size > 5) {
            markValid(input);
            return true;
        } else {
            markInvalid(
                input,
                "Password must have at least 5 unique characters."
            );
        }
    },
};

/**
 *
 * @param {HTMLInputElement} input
 */
function validateInput(input) {
    // Check browser's default validation first
    if (input.checkValidity()) {
        if (customValidators[input.id]) {
            return customValidators[input.id](input);
        } else {
            markValid(input);
            return true;
        }
    } else {
        markInvalid(input, input.validationMessage);
        return false;
    }
}

function validateForm() {
    let isValid = true;

    inputs.forEach((input) => {
        isValid = validateInput(input);
    });

    if (isValid) {
        form.submit();
    }
}
