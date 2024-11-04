function switchTab(tabName) {
    // Remove active class from all tabs and forms
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.form-container > div').forEach(form => form.classList.remove('active'));

    // Add active class to selected tab and form
    document.querySelector(`.tab:nth-child(${tabName === 'login' ? '1' : '2'}`).classList.add('active');
    document.getElementById(tabName).classList.add('active');
}

async function handleLogin(event) {
    event.preventDefault();
    const form = event.target;
    const email = form.querySelector('input[type="email"]').value;
    const password = form.querySelector('input[type="password"]').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Login successful:', data);
            window.location.href = 'http://127.0.0.1:8000/chat/';
        } else {
            const error = await response.json();
            console.error('Login failed:', error);
        }
    } catch (error) {
        console.error('Error during login:', error);
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const form = event.target;
    const inputs = form.querySelectorAll('input');
    const [email, name, password, confirmPassword] = inputs;

    if (password.value !== confirmPassword.value) {
        confirmPassword.nextElementSibling.style.display = 'block';
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/auth/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email.value,
                name: name.value,
                password: password.value,
                password_check: confirmPassword.value
            }),
        });

        if (response.ok) {
            const data = await response.json();
            // Handle successful registration
            console.log('Registration successful:', data);
            // Optionally switch to login tab
            switchTab('login');
        } else {
            const error = await response.json();
            console.error('Registration failed:', error);
        }
    } catch (error) {
        console.error('Error during registration:', error);
    }
}

// Simple form validation
document.querySelectorAll('input').forEach(input => {
    input.addEventListener('input', function() {
        const error = this.nextElementSibling;

        switch(this.type) {
            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                error.style.display = emailRegex.test(this.value) ? 'none' : 'block';
                break;
            case 'password':
                error.style.display = this.value.length >= 6 ? 'none' : 'block';
                break;
            case 'text': // name field
                error.style.display = this.value.length >= 2 ? 'none' : 'block';
                break;
        }
    });
});