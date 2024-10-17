$(document).ready(function () {
    function loadMovies() {
        $.get("/movies", function (data) {
            data.forEach(movie => {
                const movieRow = `
                    <tr>
                        <td>${movie.title}</td>
                        <td>${movie.rating}</td>
                        <td>${movie.rating_IMDb}</td>
                        <td>${movie.genre}</td>
                        <td>${movie.director}</td>
                        <td>
                            <img src="${movie.image_path}" 
                                alt="${movie.title}" 
                                height="80" 
                                class="movie-image"
                                data-description="${movie.description}">
                        </td>
                    </tr>
                `;
                $("#movieTable").append(movieRow);
            });

            // Привязываем обработчик нажатия к каждому изображению
            $(".movie-image").click(function () {
                const description = $(this).data("description");
                $("#modalDescription").text(description);
                $("#descriptionModal").modal("show");
            });
        });
    }

    $("#loadMovies").click(function () {
        $.post("/movies/load", function () {
            $("#movieTable").empty(); // Очистка таблицы перед новой загрузкой
            loadMovies();
        });
    });

    loadMovies();
});
