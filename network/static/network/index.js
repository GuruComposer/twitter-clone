$(document).ready( () => {

    // Use top nav-links to toggle between views
    document.querySelector('#all-posts-link').addEventListener('click', () => load_view('all-posts-view'));
    document.querySelector('#following-posts-link').addEventListener('click', () => load_view('following-posts-view'));
    profile_links = document.querySelectorAll('.profile-link');
    for (const profile_link of profile_links) {
        profile_link.addEventListener('click', () => load_view('profile-view'));
    }

    // By default, load all-posts
    // load_view('all-posts-view');
    
    const edit_buttons = document.querySelectorAll(".edit-button");
    const done_buttons = document.querySelectorAll(".done-button");
    
    // gather post ids.
    var post_ids = [];
    for (edit_button of edit_buttons) {
        post_ids.push(edit_button.value);
    }
    // console.log(post_ids);
    
    // hide done_button(s)
    for (const done_button of done_buttons) {
        done_button.style.display = 'none';
    }
    
    // install edit buttons
    for (const edit_button of edit_buttons) {
        // console.log(`edit_button.id = ${edit_button.value}`);
        edit_button.addEventListener('click', () => {
            // assign functionality to edit button
            console.log(edit_button.value);
            post_text_span = document.querySelector(`#post-text-${edit_button.value}`);
            current_text = post_text_span.innerHTML;
            console.log(current_text);
            textarea = document.querySelector(`#post-textarea-${edit_button.value}`);
            console.log(textarea.id);
            textarea.value = current_text;
            post_text_span.style.display = 'none';
            textarea.style.display = 'block';
            edit_button.disabled = true;
            
            
            
            // replace edit button with done button
            post_id = edit_button.value;
            done_button = document.querySelector(`#done-button-${post_id}`);
            done_button.disabled = false;
            edit_button.style.display = 'none';
            done_button.style.display = 'block';
            
            
            // assigning functionality to done button
            done_button.addEventListener('click', () => {
                edited_text = document.querySelector(`#post-textarea-${post_id}`).value;
                console.log(edited_text);
                post_text_span.innerHTML = edited_text;
                textarea.style.display = 'none';
                post_text_span.style.display = 'block';
                
                // reinitialize buttons
                done_button.disabled = true;
                edit_button.disabled = false;
                done_button.style.display = 'none';
                edit_button.style.display = 'block';
                
                // update database by hitting the API
                fetch_url = (`/update_post/${post_id}`);
                console.log(fetch_url);
                fetch(fetch_url, {
                    method: 'PUT',
                    body: JSON.stringify({
                        text: edited_text
                    })
                })
                .then( () => {
                    
                }); 
            })
        });
    }
    
    // install like buttons
    const like_buttons = document.querySelectorAll(".like-button");
    for (const like_button of like_buttons) {
        console.log(like_button.id);
        post_id = like_button.value;
        document.querySelector(`#like-button-${post_id}`).addEventListener('click', () => {

            console.log(`Clicked on: ${like_button.value}`); 
            // update database by hitting the API
            fetch_url = (`/update_post/${like_button.value}`);
            console.log(fetch_url);
            fetch(fetch_url, {
                method: 'PUT',
                body: JSON.stringify({
                    liked: "liked"
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log("success");
                console.log(data);
                console.log(data.data);
                document.querySelector(`#like-button-${like_button.value}`).innerHTML = `${data.data} <i class="fas fa-heart"></i>`;
            }); 
        })
    }
});

function load_view(view) {
  
    // Show the view and hide other views
    if (view === 'all-posts-view') {
        console.log('all-posts-view');
        document.querySelector('#following-posts-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'none';
        document.querySelector('#all-posts-view').style.display = 'block';

    }
    else if (view === 'following-posts-view') {
        console.log('following-posts-view');
        document.querySelector('#all-posts-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'none';
        document.querySelector('#following-posts-view').style.display = 'block';
    }
    else if(view === 'profile-view') {
        console.log('profile-view');
        document.querySelector('#following-posts-view').style.display = 'none';
        document.querySelector('#all-posts-view').style.display = 'none';
        document.querySelector('#profile-view').style.display = 'block';
    }
  }