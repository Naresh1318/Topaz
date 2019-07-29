let index = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        current_page: "home",
        projects: [],
    },
    methods: {
        navigate_to: function(page) {
            if (page === "projects") {
                axios.get("/public_repos")
                .then(function(response) {
                    index.projects = response["data"]["repos"]  // TODO: Add error checking
                })
            }
            this.current_page = page
        }
    },
})
