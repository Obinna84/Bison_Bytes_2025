// Get references to the price, shares input, buttons, and confirm purchase button
const priceElement = document.getElementById('price');
const sharesInput = document.getElementById('shares');
const increaseButton = document.getElementById('increase');
const decreaseButton = document.getElementById('decrease');
const buyButton = document.getElementById('buy'); // Confirm purchase button

// Base price per share
const basePrice = 100;

// Function to update the price based on the number of shares
function updatePrice() {
    const shares = parseInt(sharesInput.value, 10);
    if (shares < 1) {
        sharesInput.value = 1; // Ensure the minimum value is 1
    }
    const totalPrice = basePrice * shares; // Calculate the total price
    priceElement.textContent = totalPrice.toFixed(2); // Update the price display
}

// Event listener for the increase button
increaseButton.addEventListener('click', () => {
    sharesInput.value = parseInt(sharesInput.value, 10) + 1; // Increment shares
    updatePrice(); // Update the price
});

// Event listener for the decrease button
decreaseButton.addEventListener('click', () => {
    const currentShares = parseInt(sharesInput.value, 10);
    if (currentShares > 1) { // Ensure shares don't go below 1
        sharesInput.value = currentShares - 1; // Decrement shares
        updatePrice(); // Update the price
    }
});

// Event listener for the shares input
sharesInput.addEventListener('input', updatePrice);

// Event listener for the confirm purchase button
buyButton.addEventListener('click', () => {
    const shares = parseInt(sharesInput.value, 10);
    const totalPrice = basePrice * shares;
    alert(`You have purchased ${shares} shares for $${totalPrice.toFixed(2)}.`); // Confirmation message
});

// Initialize the price on page load
updatePrice();
