function loginManager(e) {
  e.preventDefault();

  const managerData = {
    email: document.getElementById("email").value,
    password: document.getElementById("password").value
  }

  fetch("/api/manager/login", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(managerData)
  }).then(async res => {
    const data = await res.json();
    alert(data.message);
    if (res.status == 200) {
      window.localStorage.setItem("token", data.token);
      window.location.replace("/manager")
    }   
  }).catch(err => {
    console.log(err);
    alert("something went wrong");
  })
}

window.onload = () => {
  if (window.localStorage.getItem("token")) {
    window.location.replace("/manager");
  }
}
