document.addEventListener("DOMContentLoaded", function () {
    let submitButton = document.getElementById("submit-post");
    let commentBox = document.getElementById("comment");
    let recentPosts = document.getElementById("recent-posts");

    if (!submitButton || !commentBox || !recentPosts) {
        console.error("Missing required elements: Check IDs in HTML.");
        return;
    }

    submitButton.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent default button behavior

        let commentText = commentBox.value.trim();
        
        if (commentText === "") {
            alert("Please enter a comment before submitting.");
            return;
        }

        // Create a wrapper div with class "post"
        let postWrapper = document.createElement("div");
        postWrapper.classList.add("post");

        // Create a container for profile image and text
        let contentWrapper = document.createElement("div");
        contentWrapper.classList.add("post-content"); // Add a new class for content wrapper

        // Add profile image
        let profileImg = document.createElement("img");
        profileImg.src = "../static/profile.png";  // Adjust path if necessary
        profileImg.alt = "User Profile";
        profileImg.classList.add("profile-img"); // Add a class for profile image

        // Add text content
        let postText = document.createElement("span");
        postText.textContent = commentText;
        postText.classList.add("post-text"); // Add a class for post text

        // Append elements inside the content wrapper
        contentWrapper.appendChild(profileImg);
        contentWrapper.appendChild(postText);

        // Append content wrapper to post div
        postWrapper.appendChild(contentWrapper);

        // Prepend new post to Recent Posts section
        recentPosts.prepend(postWrapper);

        // Clear textarea after posting
        commentBox.value = "";

        console.log("New post added:", commentText);
    });
});
