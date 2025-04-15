document.addEventListener('DOMContentLoaded', function () {
    const typeSelect = document.getElementById('id_type');
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');

    if (typeSelect) {
        typeSelect.addEventListener('change', function () {
            const typeId = this.value;
            fetch(`/api/dynamic/categories/?type_id=${typeId}`)
                .then(response => response.json())
                .then(data => {
                    categorySelect.innerHTML = '<option value="">---------</option>';
                    subcategorySelect.innerHTML = '<option value="">---------</option>';
                    data.forEach(category => {
                        const option = document.createElement('option');
                        option.value = category.id;
                        option.text = category.name;
                        categorySelect.appendChild(option);
                    });
                });
        });
    }

    if (categorySelect) {
        categorySelect.addEventListener('change', function () {
            const categoryId = this.value;
            fetch(`/api/dynamic/subcategories/?category_id=${categoryId}`)
                .then(response => response.json())
                .then(data => {
                    subcategorySelect.innerHTML = '<option value="">---------</option>';
                    data.forEach(subcategory => {
                        const option = document.createElement('option');
                        option.value = subcategory.id;
                        option.text = subcategory.name;
                        subcategorySelect.appendChild(option);
                    });
                });
        });
    }
});