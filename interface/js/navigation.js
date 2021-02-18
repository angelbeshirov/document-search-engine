// (function buildNavigation() {
//     var navigation = document.querySelector("#navigation-bar");
//     console.log(navigation)
//     navigation.innerHTML = "";
//     var ul = document.createElement("ul");

//     var liLogin = document.createElement("li");
//     var aLogin = document.createElement("a");
//     aLogin.innerHTML = "Експортиране";
//     aLogin.href = "";
//     aLogin.classList.add("navigation");

//     liLogin.appendChild(aLogin);

//     var liType = document.createElement("li");
//     var aType = document.createElement("a");
//     aType.innerHTML = "Вид търсене";
//     aType.href = "";
//     aType.classList.add("navigation");

//     liType.appendChild(aType);

//     ul.appendChild(liLogin);
//     ul.appendChild(liType)

//     navigation.appendChild(ul);
// }());


// function addNavigationElementsForNotLoggedUser(ul) {
//     var liHome = document.createElement("li");
//     var aHome = document.createElement("a");
//     aHome.href = "index.html";
//     aHome.classList.add("navigation");
//     aHome.classList.add("fas");
//     aHome.classList.add("fa-home");

//     var liLogin = document.createElement("li");
//     var aLogin = document.createElement("a");
//     aLogin.innerHTML = "Вход";
//     aLogin.href = "login.html";
//     aLogin.classList.add("navigation");

//     var liRegister = document.createElement("li");
//     var aRegister = document.createElement("a");
//     aRegister.innerHTML = "Регистрация";
//     aRegister.href = "register.html";
//     aRegister.classList.add("navigation");

//     liRegister.appendChild(aRegister);
//     liLogin.appendChild(aLogin);
//     liHome.appendChild(aHome);

//     ul.appendChild(liRegister);
//     ul.appendChild(liLogin);
//     ul.appendChild(liHome);
// }

// function addNavigationElementsForLoggedUser(ul) {
//     var liHome = document.createElement("li");
//     var aHome = document.createElement("a");
//     aHome.href = "index.html";
//     aHome.classList.add("navigation");
//     aHome.classList.add("fas");
//     aHome.classList.add("fa-home");

//     var liMyEdits = document.createElement("li");
//     var aMyEdits = document.createElement("a");
//     aMyEdits.innerHTML = "Моите обработки";
//     aMyEdits.href = "my_edits.html";
//     aMyEdits.classList.add("navigation");

//     var liMyPhotos = document.createElement("li");
//     var aMyPhotos = document.createElement("a");
//     aMyPhotos.innerHTML = "Моите снимки";
//     aMyPhotos.href = "my_photos.html";
//     aMyPhotos.classList.add("navigation");

//     var liLogout = document.createElement("li");
//     var aLogout = document.createElement("a");
//     aLogout.innerHTML = "Изход";
//     aLogout.href = "#";
//     aLogout.classList.add("navigation");
//     aLogout.addEventListener("click", function(event) { 
//         ajax("http://localhost:8081/users/logout", {}, handleResponseFromLogout);
//     });

//     liLogout.appendChild(aLogout);
//     liMyEdits.appendChild(aMyEdits);
//     liMyPhotos.appendChild(aMyPhotos);
//     liHome.appendChild(aHome);

//     ul.appendChild(liLogout);
//     ul.appendChild(liMyEdits);
//     ul.appendChild(liMyPhotos);
//     ul.appendChild(liHome);
// }

// function handleResponseFromLogout(xhr) {
//     if (xhr.status == 200) {
//         window.location = "index.html";
//     }
// }