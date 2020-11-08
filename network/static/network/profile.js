$(document).ready( () => {
    
    is_authenticated = document.querySelector('#is_authenticated').value;
    console.log(is_authenticated)
    
    is_self = document.querySelector('#is_self').value;
    console.log(is_self);
    
    if (is_authenticated === "true") {
        console.log("I'm inside");
        const user_id = document.querySelector('#user_id').value;
        console.log(user_id);
        if (is_self === "false"){
            follow_button = document.querySelector('#follow-button');
            follow_button.addEventListener('click', () => toggle_follow_user(user_id));
        }
    }
});


function toggle_follow_user(user_id) {
    fetch_url = (`/profile/${user_id}/follow`);
    console.log(fetch_url);
    fetch(fetch_url, {
        method: 'PUT',
        body: JSON.stringify({
            new_follower_id: user_id
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        console.log(result["follow-button-text"]);
        follow_button_text = result["follow-button-text"];
        follow_button = document.querySelector('#follow-button');
        follow_button.innerHTML = follow_button_text;
        
        username = result["username"];
        followee_follows_count = result["followee_follows_count"];
        console.log(result["followee_follows_count"]);
        document.querySelector('#user-followers').innerHTML = `${username} has ${followee_follows_count} followers.`;
    });   
}


