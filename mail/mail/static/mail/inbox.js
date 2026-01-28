document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");

  // send email on click of send email button
  let send_email_btn = document.querySelector(".send-email-btn");
  console.log(send_email_btn);
  send_email_btn.addEventListener("click", send_email);
  // load back sent mailbox
  load_mailbox("sent");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#email-view").style.display = "none";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {
  // load emails
  load_emails(mailbox);
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML =
    `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

// GET /emails/<mailbox>
function load_emails(mailbox) {
  fetch(`http://127.0.0.1:8000/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((email) => {
        let email_div = document.createElement("div");
        email_div.classList.add("email-div");

        // if email is unread, white background
        if (email.read === true) {
          email_div.classList.add("read");
        }

        let email_sender = document.createElement("span");
        email_sender.innerHTML = email.sender;

        let email_subject = document.createElement("span");
        email_subject.innerHTML = email.subject;

        let email_timestamp = document.createElement("span");
        email_timestamp.innerHTML = email.timestamp;

        email_div.appendChild(email_sender);
        email_div.appendChild(email_subject);
        email_div.append(email_timestamp);

        // add view_email on click
        email_div.addEventListener("click", function () {
          view_email(email.id);
        });

        if (mailbox === "inbox") {
          let archive_btn = document.createElement("button");
          archive_btn.innerHTML = "Archive";
          archive_btn.addEventListener("click", function (e) {
            fetch(`http://127.0.0.1:8000/emails/${email.id}`, {
              method: "PUT",
              body: JSON.stringify({
                archived: true,
              }),
            });
            // take care of propagations
            load_mailbox("inbox");
          });
          email_div.appendChild(archive_btn);
        }

        if (mailbox === "archive") {
          let unarchive_btn = document.createElement("button");
          unarchive_btn.innerHTML = "Unarchive";
          unarchive_btn.addEventListener("click", function () {
            fetch(`http://127.0.0.1:8000/emails/${email.id}`, {
              method: "PUT",
              body: JSON.stringify({
                archived: false,
              }),
            });
            load_mailbox("inbox");
          });
          email_div.appendChild(unarchive_btn);
        }

        // append email_div to #emails-view
        document.querySelector("#emails-view").append(email_div);
      });
    });
}

const view_email = (email_id) => {
  // handle displaying of views
  document.querySelector("#email-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#emails-view").style.display = "none";

  fetch(`http://127.0.0.1:8000/emails/${email_id}`)
    .then((res) => res.json())
    .then((email) => {
      let email_sender = document.createElement("h3");
      email_sender.innerHTML = email.sender;

      let email_recipients = document.createElement("h3");
      email_recipients.innerHTML = email.recipients.join(", ");

      let email_subject = document.createElement("h2");
      email_subject.innerHTML = email.subject;

      let email_timestamp = document.createElement("p");
      email_timestamp.innerHTML = email.timestamp;

      let email_body = document.createElement("p");
      email_body.innerHTML = email.body;

      // append to dom
      document
        .querySelector("#email-view")
        .append(
          email_sender,
          email_recipients,
          email_subject,
          email_timestamp,
          email_body,
        );
    })
    .catch((err) => console.log("error: ", err));

  fetch(`http://127.0.0.1:8000/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
};

// Send email
function send_email(e) {
  e.preventDefault();

  let recipients = document.querySelector("#compose-recipients").value;
  let subject = document.querySelector("#compose-subject").value;
  let body = document.querySelector("#compose-body").value;

  // POST /emails
  fetch("http://127.0.0.1:8000/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => response.json())
    .then((result) => console.log(result))
    .catch((err) => console.log(err));

  return false;
}
