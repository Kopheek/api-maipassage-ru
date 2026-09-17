// quotes.js
(function () {
    'use strict';

    async function fetchQuoteByAuthor(author, textEl, authorEl) {
        const apiUrl = `https://api.maipassage.ru/v2/quotes?author=${encodeURIComponent(author)}`;

        try {
            textEl.textContent = 'Загрузка...';
            authorEl.textContent = '';

            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }

            const data = await response.json();
            const quotes = data.results || [];

            if (quotes.length === 0) {
                textEl.textContent = `Цитат за авторством «${author}» не найдено.`;
                return;
            }

            // Если цитат несколько — берём случайную
            const randomIndex = Math.floor(Math.random() * quotes.length);
            const quote = quotes[randomIndex];

            textEl.textContent = quote.text;
            authorEl.textContent = `${quote.author} (c)`;

        } catch (error) {
            console.error('Не удалось загрузить цитату:', error);
            textEl.textContent = 'Не удалось загрузить цитату. Попробуйте позже.';
        }
    }

    function init() {
        // Находим все блоки с цитатами на странице
        const containers = document.querySelectorAll('[data-quote-author]');

        containers.forEach(container => {
            const author = container.getAttribute('data-quote-author');
            if (!author) return;

            const textEl = container.querySelector('[data-quote-text]');
            const authorEl = container.querySelector('[data-quote-author-name]');

            if (!textEl || !authorEl) {
                console.warn('Не найден элемент для текста или автора внутри', container);
                return;
            }

            fetchQuoteByAuthor(author, textEl, authorEl);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();