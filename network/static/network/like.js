const like_btns = document.querySelectorAll(".fa-heart");

like_btns.forEach(like_btn => {
    like_btn.addEventListener("click", event => {
        postID = event.target.getAttribute("data-id");
        counter = parseInt(document.querySelector("#like-counter-" + postID).innerText);
        console.log("Liked post " + postID);
        fetch("/like", {
            method: "PUT",
            body: JSON.stringify({
                ID: postID
            })
        })
        .then(response => response.json())
        .then(result => {
            if(result.isLiked === true) {
                event.target.setAttribute("class", "fas fa-heart");
                counter++; 
            } else {
                event.target.setAttribute("class", "far fa-heart");
                counter--;
            } 
            document.querySelector("#like-counter-" + postID).innerText = counter;
        });
        
    });
});


