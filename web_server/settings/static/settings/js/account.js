let auth = new coreapi.auth.SessionAuthentication({
    csrfCookieName: 'csrftoken',
    csrfHeaderName: 'X-CSRFToken'
});

let client = new coreapi.Client({auth: auth});

function associateSchool() {
    let user_name = document.getElementById('id_real_user_name');
    let stu_id = document.getElementById('id_school_stu_id');

    console.log(stu_id.value);
    console.log(user_name.value);

    let action = ["students", "create"];
    let params = {
        name: user_name.value,
        student_id: stu_id.value,
    };
    client.action(schema, action, params).then(function (result) {
        // Return value is in 'result'
        alert("Successfully associated")
    }).catch(function (error) {
        // Error value is in 'error'
        alert(error)
    });

    return false;
}