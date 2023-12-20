if(window.location.pathname === "/profile") {
    document.getElementById("profile").style.borderBottomColor = "#39a63c";
    document.getElementById("exit").onclick = function () {
        location.href = "/logout";
    };
}

if(window.location.pathname === "/seller") {
    document.getElementById("seller").style.borderBottomColor = "#39a63c";
    document.getElementById("new").onclick = function () {
        location.href = "/add_selling";
    };
}

if(window.location.pathname === "/manager") {
    document.getElementById("manager").style.borderBottomColor = "#39a63c";
}

if(window.location.pathname === "/help") {
    document.getElementById("help").style.borderBottomColor = "#39a63c";
}
