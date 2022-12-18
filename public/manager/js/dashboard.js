const contentIds = ['list-member', 'add-member', 'list-class', 'add-class'];
var selectedTab = 'list-member';

function loadListOfMembers() {
  const membersTable = document.getElementById("members-table");
  membersTable.innerHTML = "<tr><th>S.No</th><th>Name</th><th>Email</th><th>Phone</th><th></th><th></th></tr>";

  fetch("/api/member/details", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${window.localStorage.getItem("token")}`
    }
  }).then(async res => {
    if (res.status == 403 || res.status == 401) {
      window.localStorage.removeItem("token");
      window.location.replace("/manager/login");
    } else {
      const data = await res.json();
      console.log(data);
      if (res.status == 200) {
        data.forEach((member, index, _) => {
          const tableRow = document.createElement("tr");
          tableRow.innerHTML = `<td>${index + 1}</td><td>${member.name}</td><td>${member.email}</td><td>${member.contact}</td><td><button style="background-color:blue; color:white;">Update</button></td><td><button style="background-color:red; color:white;">Delete</button></td>`;
          membersTable.appendChild(tableRow);
        });
      }
    }
  }).catch(err => {
    console.log(err)
    alert("something went wrong")
  })
}

function loadListOfClasses() {
  const classesTable = document.getElementById("classes-table");
  classesTable.innerHTML = "<tr><th>S.No</th><th>Name</th><th>Instructor</th><th>Time</th><th>Capacity</th><th>Current Members Count</th><th></th><th></th></tr>";

  fetch("/api/gym-class/details", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${window.localStorage.getItem("token")}`
    }
  }).then(async res => {
    if (res.status == 403 || res.status == 401) {
      window.localStorage.removeItem("token");
      window.location.replace("/manager/login");
    } else {
      const classOptions = document.getElementById("gym_class");
      const data = await res.json();
      console.log(data);
      if (res.status == 200) {
        data.forEach((classData, index, _) => {
          const tableRow = document.createElement("tr");
          tableRow.innerHTML = `<td>${index + 1}</td><td>${classData.name}</td><td>${classData.instructor}</td><td>${classData.time}</td><td>${classData.capacity}</td><td>${classData.current_member_count}</td><td><button style="background-color:blue; color:white;">Update</button></td><td><button style="background-color:red; color:white;">Delete</button></td>`;
          classesTable.appendChild(tableRow);

          // loading classes in options
          const gymClassOption = document.createElement("option")
          gymClassOption.innerText = classData.name;
          gymClassOption.value = classData.id;
          classOptions.appendChild(gymClassOption);
        });
      }
    }
  }).catch(err => {
    console.log(err)
    alert("something went wrong")
  })
}

function addNewMember(e) {
  e.preventDefault();
  const nameInput = document.getElementById("name");
  const emailInput = document.getElementById("email");
  const contactInput = document.getElementById("contact");
  const membershipTypeInput = document.getElementById("membership_type");
  const gymClassInput = document.getElementById("gym_class");
  const memberData = {
    name: nameInput.value,
    email: emailInput.value,
    contact: contactInput.value,
    membership_type: membershipTypeInput.value,
    gym_class: gymClassInput.value == 'null' ? null : gymClassInput.value
  }

  fetch("/api/member/", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${window.localStorage.getItem("token")}`
    },
    body: JSON.stringify(memberData)
  }).then(async res => {
    if (res.status == 403 || res.status == 401) {
      window.localStorage.removeItem("token");
      window.location.replace("/manager/login");
    } else {
      const data = await res.json();
      console.log(data);
    }   
  }).catch(err => {
    console.log(err);
    alert("something went wrong");
  })
}

function setContentVisibility() {
  contentIds.forEach(contentId => {
    document.getElementById(contentId).style.display = 
      (contentId == selectedTab) ? "block" : "none";
    document.getElementById(`${contentId}-tab`).className = 
      (contentId == selectedTab) ? "side-nav--tabs-selected" : "side-nav--tabs";
  })
}

function setSelectedTab(tabId) {
  selectedTab = tabId;
  setContentVisibility();
}

window.onload = () => {
  // setting initial tab visibility
  setContentVisibility();

  // loading members list
  loadListOfMembers();
  loadListOfClasses();
}
