let index = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        current_page: "home",
        projects: [],
        latest_project: {},
        updated_time: "",
        updated_date: "",
    },
    methods: {
        navigate_to: function(page) {
            this.current_page = page
        },
        open_link: function(url) {
            let win = window.open(url, "_blank")
            win.focus()
        }
    },
    created: function() {
        // Get all public repos
        axios.get("/public_repos")
            .then(function(response) {
                index.projects = response["data"]["repos"]  // TODO: Add error checking
                index.latest_project = index.projects[0]
                index.updated = response["data"]["updated"]
            })
    }
})
