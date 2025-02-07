let articlesData;
let lastFetchTime = 0;
const BASE_URL = window.location.origin;

function loadJSON() {
  fetch(`${BASE_URL}/article_list.json`)
    .then(response => response.json())
    .then(data => {
      articlesData = data;
      console.log(articlesData);
      displayArticles(articlesData);
      setupSearch();
      updateResultsCounter(Object.keys(data).length);
      lastFetchTime = Date.now();
    })
    .catch(error => {
      console.error('Error loading JSON:', error);
    });
}

function checkForUpdates() {
  fetch(`${BASE_URL}/article_list.json`)
    .then(response => response.json())
    .then(newData => {
      // Compare with current data
      if (JSON.stringify(newData) !== JSON.stringify(articlesData)) {
        articlesData = newData;
        displayArticles(articlesData);
        updateResultsCounter(Object.keys(newData).length);
      }
    })
    .catch(error => {
      console.error('Error checking for updates:', error);
    });
}

function createArticleCard(article) {
  const source = article.base_url
    .replace('https://www.', '')
    .replace('https://', '')
    .replace('.com', '')
    .replace(/\/$/, '');

  return `
                <div class="card">
                    <img src="${article.img_url}" alt="${article.headline}" class="card-image">
                    <div class="card-content">
                        <div class="source">${source}</div>
                        <h2 class="card-title">${article.headline}</h2>
                        <div class="card-body collapsed">${article.article_body}</div>
                        <div class="card-date">${article.publish_date}</div>
                        <span class="read-more">Read more</span>
                        <a href="${article.url}" class="article-link" target="_blank">View original article ↗</a>
                    </div>
                </div>
            `;
}

function updateResultsCounter(count, searchTerm = '') {
  const counter = document.querySelector('.results-counter');
  if (searchTerm) {
    counter.textContent = `Found ${count} article${count !== 1 ? 's' : ''} matching "${searchTerm}"`;
  } else {
    counter.textContent = `${count} total article${count !== 1 ? 's' : ''}`;
  }
}

function displayArticles(data, searchTerm = '') {
  const container = document.getElementById('articles-container');
  const articles = Object.values(data);

  let filteredArticles = articles;
  if (searchTerm) {
    const searchLower = searchTerm.toLowerCase();
    filteredArticles = articles.filter(article =>
      article.headline.toLowerCase().includes(searchLower) ||
      article.article_body.toLowerCase().includes(searchLower)
    );
  }

  updateResultsCounter(filteredArticles.length, searchTerm);

  if (filteredArticles.length === 0) {
    container.innerHTML = `
            <div class="no-results">
                No articles found matching "${searchTerm}"
            </div>
        `;
    return;
  }

  // Always rebuild the entire container with filtered articles
  container.innerHTML = filteredArticles
    .map((article, index) => {
      const card = createArticleCard(article);
      return card.replace('class="card"',
        `class="card" style="animation: fadeInUp ${0.2 + index * 0.1}s ease forwards"`);
    })
    .join('');

  // Always setup card handlers after rebuilding the container
  setupCardHandlers();
}

function setupSearch() {
  const searchInput = document.getElementById('searchInput');
  let debounceTimeout;

  searchInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
      displayArticles(articlesData, e.target.value.trim());
    }, 300);
  });
}

function setupCardHandlers() {
  const cards = document.querySelectorAll('.card');

  cards.forEach(card => {
    const body = card.querySelector('.card-body');
    const readMore = card.querySelector('.read-more');

    // Add click handler to entire card
    card.addEventListener('click', (e) => {
      toggleCard(body, readMore);
    });

    // Prevent card toggle when clicking the external link
    card.querySelector('.article-link').addEventListener('click', (e) => {
      e.stopPropagation();
    });

    // Optional: Prevent card toggle when clicking the read more button
    // to avoid double-toggling (remove if you want both to work)
    readMore.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleCard(body, readMore);
    });
  });
}

function toggleCard(body, readMore) {
  const card = body.closest('.card');
  const isCollapsed = body.classList.contains('collapsed');

  if (isCollapsed) {
    body.classList.remove('collapsed');
    readMore.textContent = 'Show less';
    card.classList.add('expanding');
    card.classList.remove('collapsing');
  } else {
    body.classList.add('collapsed');
    readMore.textContent = 'Read more';
    card.classList.add('collapsing');
    card.classList.remove('expanding');
  }
}

// Start periodic updates when the page loads
window.onload = () => {
  loadJSON();
  // Check for updates every 30 seconds
  setInterval(checkForUpdates, 30000);
};