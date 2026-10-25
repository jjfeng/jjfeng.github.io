document.addEventListener('DOMContentLoaded', function() {
    const active = {category: 'all', topic: 'all'};
    const buttons = document.querySelectorAll('.filter-btn');
    const publications = document.querySelectorAll('.publication');

    function matches(pub, group) {
        const filter = active[group];
        if (filter === 'all') return true;
        return pub.getAttribute('data-' + (group === 'category' ? 'categories' : 'topics')).split(' ').includes(filter);
    }

    function apply() {
        let shown = 0;
        publications.forEach(function(pub) {
            const visible = matches(pub, 'category') && matches(pub, 'topic');
            pub.style.display = visible ? '' : 'none';
            if (visible) shown += 1;
        });
        // Hide year headers with no visible papers
        document.querySelectorAll('.pub-section').forEach(function(section) {
            const anyVisible = Array.from(section.querySelectorAll('.publication')).some(p => p.style.display !== 'none');
            section.style.display = anyVisible ? '' : 'none';
        });
        // Show how many papers each button would yield given the other group's selection
        buttons.forEach(function(btn) {
            const group = btn.getAttribute('data-group');
            const saved = active[group];
            active[group] = btn.getAttribute('data-filter');
            const n = Array.from(publications).filter(p => matches(p, 'category') && matches(p, 'topic')).length;
            active[group] = saved;
            btn.setAttribute('data-count', n);
            btn.disabled = n === 0;
        });
        document.querySelector('.filter-count').textContent = 'Showing ' + shown + ' of ' + publications.length + ' papers';
    }

    buttons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const group = this.getAttribute('data-group');
            active[group] = this.getAttribute('data-filter');
            document.querySelectorAll('.filter-btn[data-group="' + group + '"]').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            apply();
        });
    });
    apply();
});
