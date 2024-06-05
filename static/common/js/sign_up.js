function signUp() {
    const username = document.getElementById("username")
    const password = document.getElementById("password");
    const password_verification = document.getElementById("password_verification");
    const first_name = document.getElementById("first_name")
    const last_name = document.getElementById("last_name")
    const email = document.getElementById("email")
    const emailValid = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
    const url = document.getElementById("sign-up-form").action;

    if(!username.value || !password.value || !password_verification.value
        || !first_name.value || !last_name.value || !email.value ){
        alert("입력되지 않은 칸이 있습니다. 모두 입력해주세요!")
    }
    else if(!email.value.match(emailValid)) {
        alert('이메일 형식을 맞게 입력해주세요')
    }
    else if (password.value !== password_verification.value) {
        alert("Password와 Password Verification이 다릅니다!");
    }
    else {
        const formData = new FormData();
        formData.append('username', username.value);
        formData.append('password', password.value);
        formData.append('password_verification', password_verification.value);
        formData.append('first_name', first_name.value);
        formData.append('last_name', last_name.value);
        formData.append('email', email.value);

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('이미 가입한 아이디이거나, 특정 칸의 입력이 너무 깁니다.');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            window.location.href = login_url;
        })
        .catch(error => {
            alert("Error: " + error.message);
        });
    }
}