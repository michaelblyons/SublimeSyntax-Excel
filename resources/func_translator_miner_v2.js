async function waitForPageLoad() {
    await new Promise(resolve => {
        const interval = setInterval(() => {
            if (document.readyState === 'complete') {
                clearInterval(interval);
                resolve();
            }
        }, 100); // Checks every 100ms
    });
}

async function waitForElement(selector, timeout = 5000) {
    return new Promise((resolve, reject) => {
        const startTime = Date.now();
        const checkElement = setInterval(() => {
            const element = document.querySelector(selector);
            if (element) {
                clearInterval(checkElement);
                resolve(element);
            }
            if (Date.now() - startTime > timeout) {
                clearInterval(checkElement);
                reject(new Error(`Timeout waiting for ${selector}`));
            }
        }, 100);
    });
}

// Utility function to wait for a dropdown value to change
// There turned out to be duplicate dropdown options (Portuguese and Bangla) that I was mistaking for loop 'skips,' so this is probably unnecessary/redundant.
async function waitForDropdownChange(dropdown, expectedValue, timeout = 5000) {
    const startTime = Date.now();
    while (dropdown.value !== expectedValue && Date.now() - startTime < timeout) {
        await new Promise(resolve => setTimeout(resolve, 100)); // Wait 100ms before checking again
    }

    if (dropdown.value !== expectedValue) {
        throw new Error(`Dropdown value did not change to ${expectedValue} within timeout.`);
    }
}

let cliDropdown = await waitForElement("#clientCultureDropDown");

// Get the number of options in the dropdown
const numberOfOptions = cliDropdown.options.length;

// Create a text file to store the output
let outputText = "";

// Uncomment and remove integer after `i <=` to exit debug mode.
for (let i = 1; i <= 2 /* numberOfOptions */; i++) {
    await waitForPageLoad();

    let cliDropdown = await waitForElement("#clientCultureDropDown");
    let thisOption = cliDropdown.querySelector(`option:nth-child(${i})`);

    outputText += `LANG~${thisOption.innerHTML.trim()} (${thisOption.value})\n`;
    thisOption.selected = true;
    cliDropdown.dispatchEvent(new Event("change"));

    // Wait for the dropdown value to be confirmed as changed
    await waitForDropdownChange(cliDropdown, thisOption.value);

    await waitForPageLoad();

    let backButton = await waitForElement('[uib-tooltip="Go back"]');
    backButton.click();

    await waitForPageLoad();

    let funcDropdown = await waitForElement("#functionCategoryDropdown");
    funcDropdown.value = "All";
    funcDropdown.dispatchEvent(new Event("change"));

    // Wait for the dropdown value to change (optional, depending on the behavior)
    await waitForDropdownChange(funcDropdown, "All");

    let thisRefTable = await waitForElement("#referenceTable");

    const elements = thisRefTable.querySelectorAll("[title], [lang]");

    elements.forEach(el => {
        const title = el.getAttribute("title");
        const lang = el.getAttribute("lang");
        const href = el.getAttribute("href");

        if (!lang && title !== "Toggle sorting") {
            const queryValue = href?.replace("#!/ws/dictionary?query=", "");
            outputText += `${queryValue}~${title}\n`;
        } else {
            if (lang !== null) {
                outputText += `${lang}~`;
            }
        }
    });

    let preferencesButton = await waitForElement('[ui-sref="preferences"]');
    preferencesButton.click();

    await waitForPageLoad();
}

// Create a Blob from the output text and download it
const blob = new Blob([outputText], { type: 'text/plain' });
const link = document.createElement('a');
link.href = URL.createObjectURL(blob);
link.download = 'output.txt';
link.click();
