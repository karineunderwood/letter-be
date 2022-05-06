'use strict';

const likeButtonArray = document.querySelectorAll(".likes");
console.log(likeButtonArray);

for (const likeButton of likeButtonArray) {
    likeButton.addEventListener("click", () => {
        alert("Thank you for your like!");
    })
}



const quoteBtn = document.getElementById("affirmation-button");
console.log('reached here!')
console.log(quoteBtn);

if (quoteBtn) {
    quoteBtn.addEventListener('click', () => {
    fetch('/show_affirmations')
        .then(response => response.text())
        .then(affirmation => {
            document.getElementById("quote").innerHTML = affirmation;
        });
    });
} 


const emailButton = document.querySelector("#email-letter-button");
console.log(emailButton)

if (emailButton) {
    emailButton.addEventListener('click', () => {
        console.log("Clicked email button!");
        
        const formInputs = {
            letterBody: document.querySelector("#email-letter-body").value
        };

        fetch('/send_email', {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {
              'Content-Type': 'application/json',
            },
          })
            .then((response) => response.text())
            .then((responseEmail) => {
              alert(responseEmail);
            });
        
    });
}




