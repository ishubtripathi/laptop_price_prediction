document.getElementById('prediction-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    // Get form data
    const formData = new FormData(event.target);
    const brand = formData.get('brand');
    const ram = formData.get('ram');
    const storage = formData.get('storage');
    const processor = formData.get('processor');
    const gpu = formData.get('gpu');
    const os = formData.get('os');

    // Prepare data to send
    const dataToSend = {
        brand: brand,
        ram: ram,
        storage: storage,
        processor: processor,
        gpu: gpu,
        os: os
    };

    // Send data to Flask API
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    });

    const result = await response.json();

    // Display the prediction
    const resultElement = document.getElementById('result');
    if (result.error) {
        resultElement.innerText = `Error: ${result.error}`;
        resultElement.classList.add('alert-danger');
        resultElement.classList.remove('d-none', 'alert-info');
    } else {
        resultElement.innerText = `Predicted Price: $${result.prediction.toFixed(2)}`;
        resultElement.classList.remove('d-none', 'alert-danger');
        resultElement.classList.add('alert-info');
    }
});
