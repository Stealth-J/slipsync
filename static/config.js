  
  
const body = document.body;
const darkModeBtn = document.getElementById('darkModeBtn');
const themeIcon = darkModeBtn.querySelector('i');
const savedTheme = localStorage.getItem('theme');
const hero = document.getElementById('heroImg');



if (savedTheme == 'dark'){
	body.classList.add('dark')
	themeIcon.classList.replace('bi-moon-fill', 'bi-sun-fill')
	darkModeBtn.title = "Toggle Light Mode"
	if (hero){
		hero.src = '/static/img/hero-dark.png'
	}
}

darkModeBtn.addEventListener('click', function() {
	const isDark = body.classList.toggle('dark')

	if (isDark) {
		localStorage.setItem('theme', 'dark');
		body.classList.add('dark')
		themeIcon.classList.replace('bi-moon-fill', 'bi-sun-fill')
		darkModeBtn.title = "Toggle Light Mode"
		if (hero){
			hero.src = '/static/img/hero-dark.png'
		}
	} else {
		localStorage.setItem('theme', 'light');
		body.classList.remove('dark')
		themeIcon.classList.replace('bi-sun-fill', 'bi-moon-fill')
		darkModeBtn.title = "Toggle Dark Mode"
		if (hero){
			hero.src = '/static/img/hero.png'
		}
	}
})

// to prevent that error that shows when theres an active btn in an hidden item
document.addEventListener("hide.bs.modal", function (event) {
	if (document.activeElement) {
		document.activeElement.blur();
	}
});    

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  sidebar.classList.toggle('show');
  backdrop.classList.toggle('d-none');
}

document.querySelector("form")?.addEventListener("submit", function (e) {
	e.preventDefault();
	const email = document.getElementById("newsletterEmail").value;
	const errorDiv = this.querySelector(".text-danger");

	if (!email || !email.includes("@")) {
		errorDiv.style.display = "block";
	} else {
		errorDiv.style.display = "none";
		alert("Subscribed successfully!");
		this.reset();
	}
});

