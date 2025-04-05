// Get elements
const modal = document.getElementById("demoVideoModal");
const demoButton = document.getElementById("demoButton");
const closeButton = document.querySelector(".demo-close-btn");
const video = document.querySelector(".demo-responsive-video");

// Show modal on button click
demoButton.addEventListener("click", () => {
  modal.style.display = "block"; // Show the modal
});

// Hide modal on close button click
closeButton.addEventListener("click", () => {
  modal.style.display = "none"; // Hide the modal
  video.pause(); // Pause the video
  video.currentTime = 0; // Reset the video to the beginning
});

// Hide modal when clicking outside the content
window.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.style.display = "none"; // Hide the modal
    video.pause(); // Pause the video
    video.currentTime = 0; // Reset the video to the beginning
  }
});
