let auth = new coreapi.auth.SessionAuthentication({
    csrfCookieName: 'csrftoken',
    csrfHeaderName: 'X-CSRFToken'
});

let client = new coreapi.Client({auth: auth});

function updateUserInfo() {
    let first_name = document.getElementById('id_first_name');
    let last_name = document.getElementById('id_last_name');
    let id = document.getElementById('id_id');

    let action = ["users", "partial_update"];
    let params = {
        id: id.value,
        first_name: first_name.value,
        last_name: last_name.value,
    };
    console.log("Patch user info");
    client.action(schema, action, params).then(function (result) {
        // Return value is in 'result'
        alert("Successfully updated")
    }).catch(function (error) {
        // Error value is in 'error'
        alert(error)
    })
}