// // Find all elements with class "gradient"
// console.log('zzz');
// const gradientElements = document.querySelectorAll('.gradient');

// // Loop through each element with class "gradient"
// gradientElements.forEach(element => {
//   // Create an empty array to store the background color classes
//   const bgClasses = [];

//   // Loop through each class on the current element
//   for (let i = 0; i < element.classList.length; i++) {
//     const className = element.classList[i];
//     // If the class includes the string "bg", check if the last character is a number
//     if (className.includes('bg')) {
//       const lastCharacter = className.slice(-1);
//       if (!isNaN(lastCharacter)) {
//         // If the last character is a number, modify the class name to end with "-shade-X"
//         const modifiedClassName = className.replace(`-${lastCharacter}`, `-shade-${lastCharacter}`);
//         bgClasses.push(modifiedClassName);
//       } else {
//         bgClasses.push(className);
//       }
//     }
//   }

//   // If the element has any background color classes, create a gradient using those classes
//   if (bgClasses.length > 0) {
//     console.log(bgClasses);
//     const gradient = `linear-gradient(to bottom, ${bgClasses.map(className => `var(--${className})`).join(', ')})`;

//     element.style.background = gradient;
//   }
// });



const openButton = document.getElementById("burger-button");
const menu = document.getElementById("main-menu");
const closeButton = document.getElementById("close-button");

function toggleMenu() {
  menu.classList.toggle("show");
  openButton.style.display = menu.classList.contains("show") ? "none" : "block";
}

openButton.addEventListener("click", toggleMenu);

document.addEventListener("click", (event) => {
  const isMenuVisible = menu.classList.contains("show");

  if (!isMenuVisible || event.target === openButton) {
    return;
  }

  if (!menu.contains(event.target) || event.target === closeButton) {
    toggleMenu();
  }
});