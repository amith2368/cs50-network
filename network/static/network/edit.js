const edit_btns = document.querySelectorAll(".btn-edit");

edit_btns.forEach(edit_btn => {
    edit_btn.addEventListener("click", (event) => {
        const postID = event.target.getAttribute("data-id");
        let postBody = event.target.getAttribute("data-body");
        edit_btn.style.display = "none";
        activate_edit(postID, postBody, function callback(result) {
            console.log(result.message);
            edit_btn.style.display = "inline";
            allow_edit(true);
        });
        
    });
});

function activate_edit(postID, postBody, callback) {
    allow_edit(false);
    document.querySelectorAll(".edit-body").forEach(edit => {
        if(edit.getAttribute("data-id") == postID) {
            edit.value = postBody;
            edit.style.display = "block";
            edit.previousElementSibling.style.display = "none";
            
            const save_btn = document.createElement('button');
            save_btn.setAttribute("class","btn btn-primary btn-save");
            save_btn.setAttribute("data-saveid",postID);
            save_btn.innerText = "Save Changes";

            const cancel_btn = document.createElement('button');
            cancel_btn.setAttribute("class","btn btn-secondary btn-cancel ml-2");
            cancel_btn.innerText = "Discard Changes";

            edit.parentElement.appendChild(save_btn);
            edit.parentElement.appendChild(cancel_btn);

            document.querySelector(".btn-save").addEventListener("click", event => {
                fetch('/edit',{
                    method: "PUT",
                    body: JSON.stringify({
                        ID: postID,
                        body: edit.value 
                    })
                })
                .then(response => response.json())
                .then(result => {
                    save_btn.remove();
                    cancel_btn.remove();
                    edit.previousElementSibling.innerHTML = result.body;
                    edit.previousElementSibling.style.display = "block";
                    edit.style.display = "none";
                    callback(result);
                })
            });

            document.querySelector(".btn-cancel").addEventListener("click", event => {
                const result = {
                    message: "Cancelled Changes"
                }
                save_btn.remove();
                cancel_btn.remove();
                edit.previousElementSibling.style.display = "block";
                edit.style.display = "none";
                callback(result);
            });
        }
    });

}


function allow_edit(action) {
    if(action === false) {
        edit_btns.forEach(edit_btn => {
            edit_btn.disabled = true;
        });
    } else {
        edit_btns.forEach(edit_btn => {
            edit_btn.disabled = false;
        });
    }
}