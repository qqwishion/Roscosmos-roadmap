document.addEventListener('DOMContentLoaded', () => {
  const stages = {
    school: { title: 'Школа', desc: 'Основы математики и физики, кружки по робототехнике.', link: '#' },
    college: { title: 'Колледж / ССУЗ', desc: 'Технические специальности: мехатроника, приборостроение.', link: '#' },
    university: { title: 'ВУЗ', desc: 'Бакалавриат и магистратура по космическим направлениям.', link: '#' },
    internship: { title: 'Стажировка', desc: 'Лаборатории, НИР, практика на предприятиях отрасли.', link: '#' },
    job: { title: 'Работа', desc: 'Инженер, разработчик, аналитик — карьерные пути в отрасли.', link: '#' }
  };

  const svg = document.getElementById('roadmap-svg');
  svg.querySelectorAll('.stage').forEach(g => {
    const key = g.getAttribute('data-stage');
    g.style.cursor = 'pointer';

    // hover — всплывающая подсказка (title)
    const title = stages[key] ? stages[key].title : key;
    g.setAttribute('data-title', title);

    g.addEventListener('mouseenter', () => {
      g.querySelector('.stage-box').classList.add('stage-box--hover');
    });
    g.addEventListener('mouseleave', () => {
      g.querySelector('.stage-box').classList.remove('stage-box--hover');
    });

    g.addEventListener('click', () => {
      const info = document.getElementById('stage-info');
      const st = stages[key] || {title:key, desc:'—', link:'#'};
      document.getElementById('stage-title').textContent = st.title;
      document.getElementById('stage-desc').textContent = st.desc;
      document.getElementById('stage-link').href = st.link;
      info.style.display = 'block';
      info.scrollIntoView({behavior: 'smooth', block: 'center'});
    });
  });
});
