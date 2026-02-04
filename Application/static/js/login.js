document.addEventListener("DOMContentLoaded", () => {
  // Find all login forms
  const loginForms = document.querySelectorAll("form");

  loginForms.forEach(form => {
    form.addEventListener("submit", function (e) {
      let emailInput = form.querySelector("input[type='email']");
      let idInput = form.querySelector("input[name='admin_id']");
      let passwordInput = form.querySelector("input[type='password']");

      // Common validation
      if (emailInput && emailInput.value.trim() === "") {
        alert("Please enter your Email.");
        e.preventDefault();
        return;
      }

      if (idInput && idInput.value.trim() === "") {
        alert("Please enter your Admin ID.");
        e.preventDefault();
        return;
      }

      if (passwordInput && passwordInput.value.trim() === "") {
        alert("Please enter your Password.");
        e.preventDefault();
        return;
      }

      // Email validation (only for email inputs)
      if (emailInput) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailInput.value.trim())) {
          alert("Please enter a valid email address.");
          e.preventDefault();
          return;
        }
      }

      // Password length check
      if (passwordInput && passwordInput.value.length < 6) {
        alert("Password must be at least 6 characters.");
        e.preventDefault();
        return;
      }
    });
  });
});
