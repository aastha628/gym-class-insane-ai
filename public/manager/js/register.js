function registerManager(e) {
  e.preventDefault()

  const managerData = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value
  }

  fetch("/api/manager/register", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(managerData)
  }).then(async res => {
    const data = await res.json();
    alert(data.message)
    if (res.status == 200) {
      window.location.replace("/manager/login")
    }
  }).catch(err => {
    console.log(err);
    alert("Something went wrong!")
  })
}

window.onload = () => {
  if (window.localStorage.getItem("token")) {
    window.location.replace("/manager");
  }
}
