// Cargar datos de los suscriptores
fetch('suscriptores.json')
    .then(response => {
        if (!response.ok) throw new Error('Error al cargar suscriptores.json');
        return response.json();
    })
    .then(cardsData => {
        console.log('Datos de suscriptores cargados:', cardsData);
        const steamCards = document.querySelector('.js-steamCards');

        cardsData.forEach((card, index) => {
            steamCards.insertAdjacentHTML('beforeend', `
                <div class="p-2 w-1/3">
                    <div class="bg-gray-800 rounded-lg shadow-lg overflow-hidden js-steamCard transform transition duration-300 hover:scale-110 hover:shadow-xl">
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
                const steamCardsContainer = document.querySelector('.js-steamCards');
                steamCardsContainer.scrollTo({ top: 0, behavior: 'smooth' });
                setTimeout(() => {
                    activateCard(0);
                }, 1500); // Espera un segundo antes de reiniciar
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
            }, 1500);
        }

        activateCard(0);
    })
    .catch(error => console.error('Error loading the card data:', error));
// Cargar datos del podio
fetch('bits.json')
    .then(response => {
        if (!response.ok) throw new Error('Error al cargar bits.json');
        return response.json();
    })
    .then(bitsData => {
        console.log('Datos del podio cargados:', bitsData);
        const podioContainer = document.getElementById('podio-container');

        // Limpiar el contenedor del podio antes de añadir nuevos elementos
        podioContainer.innerHTML = '';

        // Seleccionar solo los primeros 3 puestos
        const topThree = bitsData.filter(user => user.rank <= 3);

        topThree.forEach(user => {
            const podioItem = document.createElement('div');
            
            // Aplicar colores específicos según el rango
            let colorClass, heightClass;
            switch (user.rank) {
                case 1:
                    colorClass = 'bg-blue-500'; // Primer lugar - Oro
                    heightClass = 'first-place';
                    break;
                case 2:
                    colorClass = 'bg-green-500'; // Segundo lugar - Plata
                    heightClass = 'second-place';
                    break;
                case 3:
                    colorClass = 'bg-red-500'; // Tercer lugar - Bronce
                    heightClass = 'third-place';
                    break;
                default:
                    colorClass = 'bg-gray-500'; // Color por defecto
            }

            podioItem.className = `podio-item ${colorClass} ${heightClass} mx-4 animate-grow`;

            podioItem.innerHTML = `
                <div class="flex flex-col items-center justify-center h-full">
                    <img src="${user.profile_image_url}" alt="${user.user_name}" class="w-1/2 h-auto mb-4"> <!-- Imagen del usuario -->
                    <div class="p-4 text-center">
                        <p class="text-2xl font-bold">${user.user_name}</p>
                        <p class="text-xl text-gray-300">Bits: ${user.score}</p>
                    </div>
                </div>
            `;

            podioContainer.appendChild(podioItem);
        });
    })
    .catch(error => console.error('Error loading the bits data:', error));
