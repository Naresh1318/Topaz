let index = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        current_page: "home",
        projects: [],
        blogs: [],
        latest_project: {},
        updated: "",
        title: "",
        description: "",
        url: ""
    },
    methods: {
        navigate_to: function(page) {
            this.current_page = page
        },
        open_link: function(url) {
            let win = window.open(url, "_blank")
            win.focus()
        },
        get_blogs: function() {
            // Get all blogs
            axios.get("/blogs")
                .then(function(response) {
                    index.blogs = response["data"]["blogs"]
                })
        },
        submit_blog: function() {
            axios.post("/blogs", {
                "title": index.title,
                "description": index.description,
                "url": index.url
            })
                .then(function(response) {
                    index.get_blogs()  // Refresh blogs list
                    console.log(response.data)
                })
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
        this.get_blogs()
    }
})
