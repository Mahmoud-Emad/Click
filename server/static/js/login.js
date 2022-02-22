let login_field = document.querySelector('#login_field');
let password = document.querySelector('#password__');

var btn = document.querySelector('#btn-submt')
btn.addEventListener("click", () => {
    if(!login_field.value.trim() || !password.value.trim()) {
        return false
    }
    else {
        loginUser(login_field, password)
    }
});

function loginUser(login_field, password) {
    const data = {login_field :login_field.value, password :password.value}
    fetch('http://127.0.0.1:8000/api/auth/sign-in/', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.Data.access_token){
                const token = data.Data.access_token
                localStorage.setItem('token', 'Bearer ' + token)
                localStorage.setItem('userId', data.Data.id)
                window.location.href = '/'
            }else{
                onMessage = document.querySelector('.wrong-email')
                onMessage.style.display = 'block'
            }
        })
        .catch((error) => {
        console.error('Error:', error);
    });
}