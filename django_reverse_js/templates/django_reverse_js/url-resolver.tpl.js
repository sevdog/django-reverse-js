{{ js_name }} = (function () {
    var data = {{ data }};
    {% include reversejs_template %}
    return data ? resolverFactory.factory(data) : resolverFactory.factory;
})();
