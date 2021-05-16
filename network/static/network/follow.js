const follow_btn = document.querySelector("#follow-btn");
var follow_count = document.querySelector("#follow-count").textContent;
var int_count = parseInt(follow_count);

follow_btn.addEventListener('click', (event) => {
    let action = true;
    if(event.target.textContent === "Follow")
        action = true
    else
        action = false
    const target_user = event.target.getAttribute('data-user');
    fetch('/follow',{
        method: "PUT",
        body: JSON.stringify({
            user: target_user,
            follow_action: action 
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        if(result.status == 201) {
            if(result.action === true) {
                follow_btn.className = "btn btn-secondary";
                follow_btn.textContent = "Unfollow"
                int_count++;
                document.querySelector("#follow-count").textContent = int_count;
            } else {
                follow_btn.className = "btn btn-primary";
                follow_btn.textContent = "Follow"
                int_count--;
                document.querySelector("#follow-count").textContent = int_count;
            }
        }
    });
});
