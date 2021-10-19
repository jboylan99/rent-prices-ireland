// Javascript function to toggle between light and dark mode.

// Button toggles between the two.
const btn = document.querySelector(".dark-toggle");

// Local Storage remembers the current theme being used on refresh.
// It gets the correct theme and displays it.
const currentTheme = localStorage.getItem("theme");
if (currentTheme == "dark-mode") {
  document.body.classList.add("dark-mode");
}
// When button is clicked it toggles.
btn.addEventListener("click", function () {
  document.body.classList.toggle("dark-mode");

// Theme is initally light mode but switches to the dark mode CSS and sets the current one to local storage.
  let theme = "light-mode";
  if (document.body.classList.contains("dark-mode")) {
    theme = "dark-mode";
  }
  localStorage.setItem("theme", theme);
});