// Small UI touches: rotate motivational quotes and simple button animations
document.addEventListener('DOMContentLoaded', () => {
  const quotes = [
    'Small progress is still progress.',
    'One habit at a time — one day at a time.',
    'Consistency compounds. Keep going!',
    'Celebrate today. Repeat tomorrow.'
  ];
  const el = document.getElementById('motivational-quote');
  if (el) {
    let idx = Math.floor(Math.random()*quotes.length);
    el.textContent = quotes[idx];
    setInterval(()=>{
      idx = (idx+1) % quotes.length;
      el.animate([{opacity:0, transform:'translateY(-6px)'},{opacity:1, transform:'translateY(0)'}],{duration:450,easing:'ease-out'});
      el.textContent = quotes[idx];
    }, 8000);
  }
  // handle complete button with remark prompt
  document.querySelectorAll('.js-complete').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const id = btn.dataset.id;
      const remark = prompt('Add a short remark for this completion (optional):', '');
      try {
        const res = await fetch(`/complete/${id}`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({remark})});
        if (res.ok) location.reload(); else alert('Error completing habit');
      } catch (err) { alert('Network error'); }
    });
  });

  // Motivation page play buttons
  document.querySelectorAll('.js-play').forEach(b => {
    b.addEventListener('click', () => {
      const text = b.dataset.text;
      if ('speechSynthesis' in window) {
        const u = new SpeechSynthesisUtterance(text);
        u.rate = 1.05;
        u.pitch = 1.05;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
      } else {
        alert('Speech synthesis not supported in this browser.');
      }
    });
  });

  const playRandom = document.getElementById('play-random');
  if (playRandom) {
    playRandom.addEventListener('click', () => {
      const items = Array.from(document.querySelectorAll('.speech-text')).map(x => x.textContent);
      const pick = items[Math.floor(Math.random()*items.length)];
      if ('speechSynthesis' in window) {
        const u = new SpeechSynthesisUtterance(pick);
        u.rate = 1.05; u.pitch = 1.05;
        window.speechSynthesis.cancel(); window.speechSynthesis.speak(u);
      }
    });
  }

  /* THEME TOGGLE + COLOR PICKERS */
  const themeToggle = document.getElementById('theme-toggle');
  const accentPicker = document.getElementById('accent-picker');
  const accent2Picker = document.getElementById('accent2-picker');

  function applyTheme(theme){
    if(theme === 'dark'){
      document.documentElement.setAttribute('data-theme','dark');
      if(themeToggle) themeToggle.textContent = 'Light Mode';
    } else {
      document.documentElement.removeAttribute('data-theme');
      if(themeToggle) themeToggle.textContent = 'Dark Mode';
    }
    localStorage.setItem('habit-theme', theme);
  }

  // initialize theme from storage or system
  const storedTheme = localStorage.getItem('habit-theme');
  const systemPref = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  applyTheme(storedTheme || systemPref);

  if(themeToggle){
    themeToggle.addEventListener('click', ()=>{
      const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      applyTheme(next);
    });
  }

  function applyAccent(a,b){
    document.documentElement.style.setProperty('--accent', a);
    document.documentElement.style.setProperty('--accent-2', b);
    localStorage.setItem('habit-accent', JSON.stringify({a,b}));
  }

  // init pickers
  const storedAcc = localStorage.getItem('habit-accent');
  if(storedAcc){
    try{const p=JSON.parse(storedAcc); if(p.a) accentPicker.value=p.a; if(p.b) accent2Picker.value=p.b; applyAccent(accentPicker.value,accent2Picker.value);}catch(e){}
  }
  if(accentPicker) accentPicker.addEventListener('input', ()=> applyAccent(accentPicker.value, accent2Picker.value));
  if(accent2Picker) accent2Picker.addEventListener('input', ()=> applyAccent(accentPicker.value, accent2Picker.value));

  /* STREAK COUNTER ANIMATION */
  document.querySelectorAll('.streak').forEach(el=>{
    const txt = el.textContent.replace(/[\u{1F300}-\u{1F6FF}\s]/gu,'').trim();
    const target = parseInt(txt) || 0;
    el.dataset.value = target;
    let start = 0;
    const duration = 900;
    const startTs = performance.now();
    function step(now){
      const t = Math.min(1,(now-startTs)/duration);
      const val = Math.floor(t*target + (1-t)*start);
      el.textContent = '🔥 ' + val;
      if(t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  });

  /* STREAK CHART (Chart.js) — build from DOM habit cards */
  const chartEl = document.getElementById('streakChart');
  if(chartEl && window.Chart){
    const labels = Array.from(document.querySelectorAll('.card')).map(c=>{ const n=c.querySelector('.habit-name'); return n ? n.textContent.trim() : 'Habit'; });
    const data = Array.from(document.querySelectorAll('.card')).map(c=>{ const s=c.querySelector('.streak'); if(!s) return 0; return parseInt((s.dataset && s.dataset.value) || s.textContent.replace(/[^0-9]/g,'')) || 0 });
    const ctx = chartEl.getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets: [{ label: 'Streaks', data, backgroundColor: labels.map(()=> getComputedStyle(document.documentElement).getPropertyValue('--accent') || '#6d28d9')} ] },
      options: { responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{y:{beginAtZero:true}} }
    });
  }
});
