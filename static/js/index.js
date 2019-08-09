let index = new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        current_page: "home",
        drawer: true,
        theme: {},
        projects: [],
        blogs: [],
        publications: [],
        top_k: [],
        latest_project: {},
        updated: "",
    },
    methods: {
        /**
         * Navigate to required page
         * @param page, page name
         */
        navigate_to: function(page) {
            this.current_page = page
            if (this.is_mobile())
                this.drawer = false
        },
        /**
         * Open URL in a new window
         * @param url
         */
        open_link: function(url) {
            let win = window.open(url, "_blank")
            win.focus()
        },
        /**
         * Get theme object and set this.theme
         */
        get_theme: function() {
          axios.get("/theme")
              .then(function(response) {
                  if(response["data"]["theme"])
                      index.theme = response["data"]["theme"]
                  else
                      console.log("ERROR: " + response["data"]["ERROR"])
              })
        },
        /**
         * Get top_k entries from the database and set this.top_k
         */
        get_top_k: function() {
            axios.get("/top_k", {
                params: {
                    "k": 3
                },
            })
                .then(function(response) {
                    index.top_k = response["data"]["top_k"]
                })
        },
        /**
         * Get all repos and set this.projects and this.latest_project
         */
        get_repos: function() {
            // Get all public repos
            axios.get("/public_repos")
                .then(function(response) {
                    index.projects = response["data"]["repos"]
                    index.latest_project = index.projects[0]
                    index.updated = response["data"]["updated"]
                })
        },
        /**
         * Get all blogs and set this.blogs
         */
        get_blogs: function() {
            // Get all blogs
            axios.get("/blogs")
                .then(function(response) {
                    index.blogs = response["data"]["blogs"]
                })
        },
        /**
         * Get all publications and set this.publications
         */
        get_publications: function() {
            // Get all publications
            axios.get("/publications")
                .then(function(response) {
                    index.publications = response["data"]["publications"]
                })
        },
        is_mobile: function() {
            if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                return true
            }
            else {
                return false
            }
        },
        card_width: function() {
            if (this.is_mobile())
                return "90%"
            else
                return "40%"
        },
        nav_margin: function() {
            if (this.is_mobile())
                return "0vh"
            else
                return "16vh"
        }
    },
    created: function() {
        this.get_theme()
        this.get_top_k()
        this.get_repos()
        this.get_blogs()
        this.get_publications()
    }
})
