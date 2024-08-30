fetch('suscriptores.json')
    .then(response => response.json())
    .then(cardsData => {
        const steamCards = document.querySelector('.js-steamCards');

        cardsData.forEach((card, index) => {
            steamCards.insertAdjacentHTML('beforeend', `
                <div class="p-2 w-1/3">
                    <div class="bg-gray-800 rounded-lg shadow-lg overflow-hidden js-steamCard transform transition duration-300 hover:scale-10 hover:shadow-xl">
                        <img src="${card.profile_image_url}" alt="${card.user_name}" class="w-full h-1/2">
                        <div class="p-5 m-2 text-center">
                            <h3 class="text-4xl font-semibold text-white">${card.user_name}</h3>
                            <p class="text-2xl text-gray-400">Regaladas: ${card.gift_count}</p>
                        </div>
                    </div>
                </div>
            `);
        });

        const cards = document.querySelectorAll('.js-steamCard');

        function activateCard(index) {
            if (index >= cards.length) {
                // Reinicia el ciclo
                document.documentElement.scrollTo({ top: 0, behavior: 'smooth' });
                setTimeout(() => {
                    activateCard(0);
                }, 1000); // Espera un segundo antes de reiniciar
                return;
            }

            cards[index].classList.add('scale-110');

            // Cada fila tiene exactamente 3 tarjetas
            const cardsPerRow = 3;
            const rowIndex = Math.floor(index / cardsPerRow);

            // Si la tarjeta está en la tercera fila o más abajo, hace scroll
            if (rowIndex >= 2) {
                cards[index].scrollIntoView({ behavior: 'smooth', block: 'start' });
            }

            setTimeout(() => {
                cards[index].classList.remove('scale-110');
                activateCard(index + 1);
            }, 1000);
        }

        activateCard(0);
    })
    .catch(error => console.error('Error loading the card data:', error));
