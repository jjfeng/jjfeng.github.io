document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');

            const publications = document.querySelectorAll('.publication');
            publications.forEach(function(pub) {
                if (filter === 'all') {
                    pub.style.display = 'block';
                } else if (pub.getAttribute('data-tags').includes(filter)) {
                    pub.style.display = 'block';
                } else {
                    pub.style.display = 'none';
                }
            });
        });
    });
});

