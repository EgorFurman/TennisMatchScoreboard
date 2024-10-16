const form = document.querySelector('form');


form.addEventListener('submit', (event) => {
    const player1 = document.querySelector('input[name="player1"]').value;
    const player2 = document.querySelector('input[name="player2"]').value;

    if (player1.trim() === player2.trim()) {
        event.preventDefault();
        alert("Player names must be different!");
    }
});


// document.addEventListener('DOMContentLoaded', function() {
//     // Получаем URL текущей страницы
//     var url = new URL(window.location.href);
//     // Получаем значение filter_by_player_name из URL
//     var filter_by_player_name = url.searchParams.get('filter_by_player_name');
//
//     // Если фильтр установлен, то устанавливаем его значение в селект
//     if (filter_by_player_name) {
//         document.getElementById('filter_by_player_name').value = filter_by_player_name;
//     }
//     else {
//         document.getElementById('filter_by_player_name').value = 'All players';
//     }
// });
