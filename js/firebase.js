const firebaseConfig = {
    apiKey: "AIzaSyD1NkPOkTXp9uZkmhKxDC5_czF8SZdZVFU",
    authDomain: "loan-approval-d0a30.firebaseapp.com",
    databaseURL: "https://loan-approval-d0a30-default-rtdb.firebaseio.com",
    projectId: "loan-approval-d0a30",
    storageBucket: "loan-approval-d0a30.appspot.com",
    messagingSenderId: "731782298620",
    appId: "1:731782298620:web:762a2c6c4acde6ac2d9079"
};


// initialize firebase
firebase.initializeApp(firebaseConfig);

// reference your database
var contactFormDB = firebase.database().ref("contactForm");

document.getElementById("contactForm").addEventListener("submit", submitForm);

function submitForm(e) {
    e.preventDefault();

    var name = getElementVal("name");
    var emailid = getElementVal("emailid");
    var msgContent = getElementVal("msgContent");

    saveMessages(name, emailid, msgContent);

    //   enable alert
    document.querySelector(".alert").style.display = "block";

    //   remove the alert
    setTimeout(() => {
        document.querySelector(".alert").style.display = "none";
    }, 3000);

    //   reset the form
    document.getElementById("contactForm").reset();
}

const saveMessages = (name, emailid, msgContent) => {
    var newContactForm = contactFormDB.push();

    newContactForm.set({
        name: name,
        emailid: emailid,
        msgContent: msgContent,
    });
};

const getElementVal = (id) => {
    return document.getElementById(id).value;
};
