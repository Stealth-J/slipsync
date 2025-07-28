  
  
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



// {'home_team': 'Linfield FC', 'away_team': 'Shelbourne FC', 'league': 'UEFA Champions League', 'start_time': '2025-07-16 18:45:00', 'status': 'Not start', 'market': '1X2', 'pick': 'Away', 'odds': '2.66'}
// {'home_team': 'FC Dinamo Minsk', 'away_team': 'Ludogorets', 'league': 'UEFA Champions League', 'start_time': '2025-07-16 18:45:00', 'status': 'Not start', 'market': 'Over/Under', 'pick': 'Under 2.5', 'odds': '1.92'}
// {'home_team': 'Linfield FC', 'away_team': 'Shelbourne FC', 'league': 'UEFA Champions League', 'start_time': '2025-07-16 18:45:00', 'status': 'Not start', 'market': 'Draw No Bet', 'pick': 'Home', 'odds': '1.90'}
// {'home_team': 'Rangers', 'away_team': 'Panathinaikos', 'league': 'UEFA Champions League', 'start_time': '2025-07-22 18:45:00', 'status': 'Not start', 'market': 'Draw No Bet', 'pick': 'Home', 
// 'odds': '1.46'}
// {'home_team': 'Port Melbourne Sharks', 'away_team': 'Dandenong Thunder', 'league': 'Victoria, NPL', 'start_time': '2025-07-18 10:15:00', 'status': 'Not start', 'market': '1X2', 'pick': 'Home', 'odds': '6.25'}
// {'home_team': 'Santos FC SP', 'away_team': 'CA Paranaense PR', 'league': 'U20 Brasileiro Serie A', 'start_time': '2025-07-16 18:00:00', 'status': 'Not start', 'market': '1X2', 'pick': 'Draw', 'odds': '3.80'}
// {'home_team': 'RB Bragantino SP', 'away_team': 'SC Internacional RS', 'league': 'U20 Brasileiro Serie A', 'start_time': '2025-07-16 18:00:00', 'status': 'Not start', 'market': '1X2', 'pick': 
// 'Home', 'odds': '1.60'}
