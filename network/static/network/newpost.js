console.log("Hola");
const newPostBtn = document.querySelector("#newPostBtn");
const postBody = document.querySelector("#newPostBody");
newPostBtn.addEventListener('click', () => {
    console.log(postBody.value);
    fetch('/newpost',{
        method: "POST",
        body: JSON.stringify({body: postBody.value})
    })
    .then(response => response.json())
    .then(result => {
        if(result.status === 201)
        {
            console.log("Post saved successfully");
            console.log(result);
            const newContent = document.createElement('div');
            newContent.innerHTML=`
            <div id="post-${result.post_id}" class="card shadow">
            <div class="card-body">
                <p>${result.username}</p>
                <p>${result.body}</p>
                <p>Posted on ${result.timestamp} </p>
                <p>Likes: 0 </p>
            </div>
            </div>`; 
            document.querySelector('#content').prepend(newContent);
            document.querySelector("#newPostBody").value = "";
        }
        
    })
    .catch(error => {
        console.log("Error", error);
    });
});