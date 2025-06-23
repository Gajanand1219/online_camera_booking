
document.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.card');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('show');
        entry.target.classList.remove('hide');
      } else {
        entry.target.classList.remove('show');
        entry.target.classList.add('hide');
      }
    });
  });
  cards.forEach(card => {
    observer.observe(card);
  });
});
// /////////////////////////////////////////////////////////////////////////////////


    document.addEventListener('DOMContentLoaded', function () {

    function handleCard(cardNumber, pricePerDay, itemName) {
        // Select necessary elements for the card
      let quantityElement = document.getElementById(`quantity${cardNumber}`);
        let totalElement = document.getElementById(`total${cardNumber}`);
        let addDayButton = document.getElementById(`addDay${cardNumber}`);
        let removeDayButton = document.getElementById(`removeDay${cardNumber}`);
        let orderNowButton = document.getElementById(`orderNow${cardNumber}`);
        let itemNameElement = document.getElementById(`itemName${cardNumber}`);

        let quantity = 0; // Initialize quantity to zero

        // Set the item name dynamically in the card
        itemNameElement.textContent = itemName;

        // Add event listener to increment days when "Add Day" is clicked
        addDayButton.addEventListener('click', function () {
            quantity++;
            updateTotal(); // Recalculate total
        });

        // Add event listener to decrement days when "Remove Day" is clicked
        removeDayButton.addEventListener('click', function () {
            if (quantity > 0) { // Ensure quantity doesn't go below 0
                quantity--;
                updateTotal(); // Recalculate total
            }
        });

        // Add event listener for the "ORDER NOW" button
        orderNowButton.addEventListener('click', function () {
            // Check if user is logged in
            fetch('/check_user')
                .then(response => response.json())
                .then(data => {
                    if (data.logged_in) {
                        // Update the modal with order details
                        document.getElementById('orderDays').textContent = quantity;
                        document.getElementById('orderTotal').textContent = (quantity * pricePerDay).toFixed(2); // Update total price in modal
                        document.getElementById('orderItemName').textContent = itemName; // Set item name in the modal
                        document.getElementById('hiddenPrice').value = pricePerDay; // Set hidden price field
                        document.getElementById('hiddenItemName').value = itemName; // Set hidden item name field

//                         // Open the modal
                        $('#orderModal').modal('show');
                    } else {
                        // If not logged in, redirect to login page
                        window.location.href = '/login';
                    }
                });
        });

        // Function to update the total displayed in the card
        function updateTotal() {
            quantityElement.textContent = quantity; // Update quantity display
            totalElement.textContent = (quantity * pricePerDay).toFixed(2); // Update total price display
        }
    }

    // Initialize all the cards with respective prices and names
    handleCard(1, 20, 'Drone');
    handleCard(2, 30, 'Photo Camera');
    handleCard(3, 40, 'Shooting Camera');
    handleCard(4, 50, 'Wedding Shooting');
    handleCard(5, 60, 'Movies Shooting');
    handleCard(6, 80, 'Party Photos Shooting');
    handleCard(7, 45, 'News Shooting');
    handleCard(8, 40, 'Small Program Photo Shoot');
});


// /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

document.addEventListener("DOMContentLoaded", function () {
  const chatButton = document.getElementById("chatButton");
  const chatContainer = document.getElementById("chatContainer");
  const chatBox = document.getElementById("chatBox");
  const userInput = document.getElementById("userInput");
  const sendButton = document.getElementById("sendButton");

  // Toggle chat visibility
  chatButton.addEventListener("click", function () {
      chatContainer.style.display = chatContainer.style.display === "none" || chatContainer.style.display === ""
          ? "block"
          : "none";
      if (chatContainer.style.display === "none") chatBox.innerHTML = ""; // Clear chat if closed
  });

  // Function to append messages with different background colors
  function appendMessage(sender, message) {
      const messageDiv = document.createElement("div");
      messageDiv.classList.add("message", sender === "user" ? "user-msg" : "ai-msg");
      messageDiv.innerHTML = message;

      chatBox.appendChild(messageDiv);
      chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to latest message
  }

  // Function to send a message to the Flask backend
  async function sendMessage(userMessage) {
      appendMessage("user", userMessage);

      try {
          const response = await fetch("/chat", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ message: userMessage })
          });

          const data = await response.json();
          if (data.response) {
              appendMessage("ai", data.response);
          } else {
              appendMessage("ai", "Sorry, I didn't understand that.");
          }
      } catch (error) {
          appendMessage("ai", "An error occurred. Please try again.");
      }
  }

  // Handle send button click
  sendButton.addEventListener("click", function () {
      const userMessage = userInput.value.trim();
      if (userMessage) {
          sendMessage(userMessage);
          userInput.value = "";
      }
  });

  // Handle Enter key press
  userInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
          sendButton.click();
      }
  });

  // Handle predefined option buttons
  document.querySelectorAll(".option-btn").forEach(button => {
      button.addEventListener("click", function () {
          const userMessage = this.getAttribute("data-option");
          sendMessage(userMessage);
      });
  });
});


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

      // Function to prevent opening of developer tools
      function preventDevTools(e) {
                if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
                    e.preventDefault();
                }
            }
            // Prevent right-click and context menu
            function preventRightClick(e) {
                e.preventDefault();
            }

            // Disable the ability to view source via browser context (disable Ctrl+U and right-click)
            document.addEventListener('keydown', function (e) {
            if ((e.ctrlKey && e.key === 'u') || (e.key === 'U')) {
                e.preventDefault();
            }
            });
            // Event listeners for keydown and context menu
            document.addEventListener('keydown', preventDevTools);
            document.addEventListener('contextmenu', preventRightClick);


// /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    let slideIndex = 0;
    const backgrounds = [
        'url("https://cdn.pixabay.com/photo/2016/10/25/17/00/camera-1769414_1280.jpg")',
        'url("https://images.pexels.com/photos/7100321/pexels-photo-7100321.jpeg?cs=srgb&dl=pexels-vlada-karpovich-7100321.jpg&fm=jpg")',
        'url("https://camerainaction.com/model/assets/img/blog/pre-wed.jpeg")',
        'url("https://www.bgcsm.org/wp-content/uploads/2024/01/2024-01-06-iDC-40489-1024x683.jpg")',
        'url("https://img.freepik.com/premium-photo/group-friends-celebrating-with-fireworks-background_662214-24721.jpg")'
    ];

    showSlides();

    function showSlides() {
        const slideshow = document.querySelector('.slideshow-container');

        slideIndex++;
        if (slideIndex > backgrounds.length) { slideIndex = 1; }

        // Set the background image
        slideshow.style.backgroundImage = backgrounds[slideIndex - 1];

        // Ensure the background covers the entire container
        slideshow.style.backgroundSize = "cover"; // Ensure the image covers the entire container
        slideshow.style.backgroundPosition = "center";

        setTimeout(showSlides, 4000); // Change image every 3 seconds
    }
// ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

document.addEventListener("DOMContentLoaded", function () {
  const navbarToggler = document.querySelector(".navbar-toggler");
  const navLinks = document.querySelectorAll(".nav-link");

  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");

      // Check if it's an internal anchor link (starts with "#")
      if (targetId.startsWith("#")) {
        e.preventDefault();

        const targetElement = document.getElementById(targetId.slice(1));
        if (targetElement) {
          // Mobile-specific behavior
          if (window.innerWidth <= 768) {
            if (window.getComputedStyle(navbarToggler).display !== "none") {
              navbarToggler.click();
            }
            const offset = 300; // Offset for mobile
            const targetPosition = targetElement.offsetTop - offset;
            window.scrollTo({
              top: targetPosition,
              behavior: "smooth",
            });
          } else {
            // Desktop-specific behavior
            const offset = 70; // Offset for desktop
            const targetPosition = targetElement.offsetTop - offset;
            window.scrollTo({
              top: targetPosition,
              behavior: "smooth",
            });
          }

        }
      }
      // If it's an external link (like "/login" or "/profile"), don't prevent default
    });
  });
});

// //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  // Show content after 5000 milliseconds (5 seconds)
  setTimeout(function() {
    document.getElementById('content').style.display = 'flex';
}, 3000);
  // Function to hide the card when the close button is clicked
  function closeCard(event) {
    event.preventDefault(); // Prevent default anchor behavior
    document.getElementById('content').style.display = 'none'; // Hide the card
}
// //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // Auto-scroll the carousel every 3 seconds
    var carousel = new bootstrap.Carousel(document.getElementById('photographersCarousel'), {
        interval: 50000,
        ride: "carousel"
    });

// ////////////////////////////////////////////////////////////////////////////////////////////////////////

// Example of dynamically changing the item name in the modal:
document.getElementById('orderModal1').addEventListener('show.bs.modal', function (event) {
  var button = event.relatedTarget; // Button that triggered the modal
  var itemName = button.getAttribute('data-item-name'); // Get data-item-name attribute from the button
  var itemText = button.getAttribute('data-item-text'); // Get data-item-text attribute from the button
  var itemContact = button.getAttribute('data-item-contact'); // Get data-item-contact attribute from the button
  var itemImage = button.getAttribute('data-item-image'); // Get data-item-image attribute from the button

  // Set dynamic content in modal
  var modalBodyName = document.querySelector('#orderItemName9');
  var modalBodyText = document.querySelector('#orderItemText');
  var modalBodyContact = document.querySelector('#orderItemContact');
  var modalImage = document.querySelector('#orderItemImage'); // Select the image element inside the modal

  modalBodyName.textContent = itemName; // Set the name
  modalBodyText.textContent = itemText; // Set the description text
  modalBodyContact.textContent = "Contact: " + itemContact; // Set the contact number
  modalImage.src = itemImage; // Set the dynamic image source

  // Dynamically update the phone number link
  var contactLink = document.querySelector('#orderItemContact');
  contactLink.href = "tel:" + itemContact; // Set the href to the dynamic phone number
});
// //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    function scrollLeft() {
        document.getElementById("scrollContainer").scrollBy({ left: -200, behavior: 'smooth' });
    }

    function scrollRight() {
        document.getElementById("scrollContainer").scrollBy({ left: 200, behavior: 'smooth' });
    }

