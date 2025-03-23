document.addEventListener("DOMContentLoaded", function () {
    const popularPostsContainer = document.getElementById("popular-posts");

    // Array of random posts
    const randomPosts = [
        { text: "This new Carti album is Fye" },
        { text: "WHEN IS FRANK GOIN DROP" },
        { text: "SWAMP IZZO" },
        { text: "Kendrick dropped a new single!" },
        { text: "Best album of 2023 so far?" },
        { text: "Travis Scott's tour was insane" },
        { text: "Who's the GOAT of rap?" },
        { text: "New Ye feature just dropped" },
        { text: "Bro, did you hear that new snippet?" },  
        { text: "This beat is straight fire, who produced it?" },  
        { text: "Album rollout is crazy rn" },  
        { text: "Who’s got the best flow in the game?" },  
        { text: "New Drake leak got me hyped" },  
        { text: "This track is a vibe, no cap" },  
        { text: "When’s the deluxe dropping?" },  
        { text: "This producer never misses" },  
        { text: "Who’s the most underrated rapper?" },  
        { text: "This hook is stuck in my head" },  
        { text: "New JID album when?" },  
        { text: "This freestyle is insane" },  
        { text: "Who’s winning the rap beef?" },  
        { text: "This collab was unexpected" },  
        { text: "Album of the year contender?" },  
        { text: "This track aged like fine wine" },  
        { text: "Who’s got the best ad-libs?" },  
        { text: "This music video is next level" },  
        { text: "New Metro project is coming soon" },  
        { text: "This artist is underrated af" },
    ];

    // Function to create a post element
    function createPost(postText) {
        const postDiv = document.createElement("div");
        postDiv.classList.add("post");

        const profileImg = document.createElement("img");
        profileImg.src = "../static/profile.png";
        profileImg.alt = "User Profile";
        profileImg.classList.add("profile-img");

        const postTextSpan = document.createElement("span");
        postTextSpan.textContent = postText;

        postDiv.appendChild(profileImg);
        postDiv.appendChild(postTextSpan);

        return postDiv;
    }

    // Function to update the popular posts section
    function updatePopularPosts() {
        // Clear existing posts
        popularPostsContainer.innerHTML = "";

        // Randomly select 3 posts from the array
        const shuffledPosts = randomPosts.sort(() => 0.5 - Math.random()).slice(0, 5);

        // Add the selected posts to the container
        shuffledPosts.forEach(post => {
            const postElement = createPost(post.text);
            popularPostsContainer.appendChild(postElement);
        });
    }

    // Update the popular posts section initially
    updatePopularPosts();

    // Update the popular posts section at random intervals (between 5 and 10 seconds)
    setInterval(updatePopularPosts, Math.floor(Math.random() * (10000 - 5000 + 1) + 5000));
});
