let currentPage = 1;
let searchQuery = '';

async function fetchArticles(page = 1, search = '') {
    let url = `/api/articles/?page=${page}`;
    if (search) {
        url += `&search=${search}`;
    }
    let response = await fetch(url);
    return await response.json();
}

    function renderArticles(articles) {
        let articlesContainer = document.getElementById('articles');
        articlesContainer.innerHTML = '';
        articles.results.forEach(article => {
            let articleElement = document.createElement('article');
            articleElement.className = 'article';
            articleElement.innerText= `
                ID: ${article.uid}
                Title: ${article.title}
                Body: ${article.body}
                Author:${article.author}
                Published on: ${article.publication_date}
            `;
            articlesContainer.appendChild(articleElement);
        });
    }

    function updatePageNumber(page) {
        const pageNumberElement = document.getElementById('page-number');
        pageNumberElement.textContent = `Page ${page}`;
    }

    async function loadArticles(page, search) {
        const articles = await fetchArticles(page, search);
        renderArticles(articles);
        updatePageNumber(page);
    }

    document.getElementById('next').addEventListener('click', () => {
        currentPage++;
        loadArticles(currentPage);
    });

    document.getElementById('prev').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadArticles(currentPage);
        }
    });

    document.getElementById('search-form').addEventListener('submit', (event) => {
        event.preventDefault();
        searchQuery = document.getElementById('search-input').value;
        currentPage = 1;
        loadArticles(currentPage, searchQuery);
    });

    loadArticles(currentPage, searchQuery);
