document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("artist-producer-info-form");

    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault(); // Prevent default form submission

            // Get form data
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            // Client-side validation
            if (!data.username || !data.firstname || !data.lastname || !data.email) {
                document.getElementById("error-message").style.display = "block";
                document.getElementById("error-message").textContent = "Please fill out all required fields.";
                return;
            }

            try {
                // Send form data to the server
                const response = await fetch("/artist-producer-information", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                });

                if (response.ok) {
                    // Redirect to artist landing page on success
                    window.location.href = "/artist-landing-page";
                } else {
                    // Handle server-side errors
                    const errorData = await response.json();
                    document.getElementById("error-message").style.display = "block";
                    document.getElementById("error-message").textContent = errorData.error || "An error occurred. Please try again.";
                }
            } catch (error) {
                console.error("Error:", error);
                document.getElementById("error-message").style.display = "block";
                document.getElementById("error-message").textContent = "An error occurred. Please try again.";
            }
        });
    }
});

// Wait until the page fully loads
document.addEventListener("DOMContentLoaded", function () {
    // Get the canvas element
    const ctx = document.getElementById("songChart").getContext("2d");

    // Create the line chart
    const songChart = new Chart(ctx, {
        type: "line", // Line chart type
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], // X-axis labels
            datasets: [
                {
                    label: "Stream Count (in millions)", // Legend label
                    data: [5, 10, 15, 12, 20, 25], // Data points
                    borderColor: "#a993f7", // Line color
                    backgroundColor: "rgba(169, 147, 247, 0.2)", // Light fill color
                    borderWidth: 2, // Line thickness
                    pointRadius: 5, // Size of points on the graph
                    pointHoverRadius: 7, // Bigger size when hovered
                    tension: 0.4, // Smooth curve
                },
            ],
        },
        options: {
            responsive: true, // Adjusts to screen size
            plugins: {
                legend: {
                    display: true,
                    position: "top",
                },
                tooltip: {
                    enabled: true, // Show tooltips on hover
                    backgroundColor: "#243b5e",
                    titleColor: "#fff",
                    bodyColor: "#fff",
                },
            },
            scales: {
                x: {
                    grid: {
                        display: false, // Hide x-axis grid lines
                    },
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: "rgba(255, 255, 255, 0.1)", // Faint grid lines
                    },
                },
            },
        },
    });
});