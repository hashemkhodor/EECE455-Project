function performOperation() {
    const operation = document.getElementById('operation').value;
    const mValue = document.getElementById('mValue').value;
    let poly1, poly2;

    // Get polynomial values based on the operation
    if (operation === 'add' || operation === 'subtract' || operation === 'multiply' || operation === 'divide') {
        poly1 = document.getElementById('poly1').value;
        poly2 = document.getElementById('poly2').value;
    } else {
        poly1 = document.getElementById('poly').value;
    }

    // Make an AJAX request to the Flask backend
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            operation,
            mValue,
            poly1,
            poly2,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Update the result on the frontend
        document.getElementById('result').innerText = `Result: ${data.result}`;

        // If the operation is 'inverse', display the steps
        if (operation === 'inverse' && data.steps) {
            const stepsContainer = document.getElementById('steps');
            stepsContainer.innerHTML = '<h3>Extended Euclidean Algorithm Steps:</h3>';
            data.steps.forEach(step => {
                stepsContainer.innerHTML += `<div>${step}</div>`;
            });
        } else {
            // Clear the steps container if the operation is not 'inverse'
            document.getElementById('steps').innerHTML = '';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = `Error: ${error.message}`;
    });
}

function handleOperationChange() {
    const operation = document.getElementById('operation').value;
    const inputBoxes = document.getElementById('inputBoxes');

    // Clear any existing input boxes
    inputBoxes.innerHTML = '';

    // Create input boxes based on the selected operation
    if (operation === 'inverse' || operation === 'modulo') {
        inputBoxes.innerHTML = '<label for="poly">Enter Polynomial:</label>' +
            '<input type="text" id="poly" required>';
    } else if (operation === 'add' || operation === 'subtract' || operation === 'multiply' || operation === 'divide') {
        inputBoxes.innerHTML = '<label for="poly1">Enter Polynomial 1:</label>' +
            '<input type="text" id="poly1" required>' +
            '<label for="poly2">Enter Polynomial 2:</label>' +
            '<input type="text" id="poly2" required>';
    }
    // Add conditions for other operations as needed
}

// Add this function to show the steps when 'Show Steps' button is clicked
function showSteps() {
    const stepsDiv = document.getElementById('steps');

    // Make an AJAX request to the Flask backend to fetch steps
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            operation: 'inverse',  // Request steps for the inverse operation
            mValue: document.getElementById('mValue').value,
            poly1: document.getElementById('poly').value,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Update the steps on the frontend
        const steps = data.steps;
        stepsDiv.innerHTML = '<h3>Extended Euclidean Algorithm Steps:</h3>';
        steps.forEach(step => {
            stepsDiv.innerHTML += `<div>${step}</div>`;
        });
    })
    .catch(error => {
        console.error('Error:', error);
        stepsDiv.innerHTML = `Error: ${error.message}`;
    });
}
