// quotes.js
(function () {
    'use strict';

    async function fetchQuote(author, subject, textEl, authorEl) {
        const params = new URLSearchParams();

        if (author) {
            params.set('author', author);
        }
        if (subject) {
            params.set('subject', subject);
        }

        const apiUrl = `https://api.maipassage.ru/v2/quotes?${params.toString()}`;

        try {
            textEl.textContent = 'Загрузка...';
            if (authorEl) {
                authorEl.textContent = '';
            }

            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }

            const data = await response.json();
            const quotes = data.results || [];

            if (quotes.length === 0) {
                // Формируем понятное сообщение, если ничего не нашли
                const parts = [];
                if (author) parts.push(`автор «${author}»`);
                if (subject) parts.push(`предмет «${subject}»`);
                textEl.textContent = `Цитат (${parts.join(', ')}) не найдено.`;
                return;
            }

            const randomIndex = Math.floor(Math.random() * quotes.length);
            const quote = quotes[randomIndex];

            textEl.textContent = quote.text;

            if (authorEl) {
                // Если у цитаты есть поле author — показываем его,
                // иначе подставляем то, что искали
                authorEl.textContent = quote.author || author || '';
            }

        } catch (error) {
            console.error('Не удалось загрузить цитату:', error);
            textEl.textContent = 'Не удалось загрузить цитату. Попробуйте позже.';
        }
    }

    function init() {
        const containers = document.querySelectorAll('[data-quote-author], [data-quote-subject]');

        containers.forEach(container => {
            const author = container.getAttribute('data-quote-author') || '';
            const subject = container.getAttribute('data-quote-subject') || '';

            if (!author && !subject) {
                console.warn('У контейнера не указан ни автор, ни предмет:', container);
                return;
            }

            const textEl = container.querySelector('[data-quote-text]');
            const authorEl = container.querySelector('[data-quote-author-name]');

            if (!textEl) {
                console.warn('Не найден элемент для текста цитаты внутри', container);
                return;
            }

            const load = () => fetchQuote(author, subject, textEl, authorEl);
            load();

            const btn = container.querySelector('[data-quote-refresh]');
            if (btn) {
                btn.addEventListener('click', load);
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();