let vue_admin = new Vue({
    el: "#app",
    vuetify: new Vuetify(),
    data: {
        projects: [],
        selected_projects: [],
        search: "",
        projects_header:
            [{text: "Title", align: "left", sorted: false, value: "title"},
             {text: "Url", value: "url"}, {text: "Primary language", value: "primary_language"},
             {text: "Stars", value: "stars"}, {text: "Timestamp", value: "timestamp"},
             {text: "Visibility", value: "visibility"}],
        blogs: [],
        publications: [],
        types: ["blog", "publication"],
        title: "",
        description: "",
        url: "",
        image_url: "",
        time_stamp: "",
        type: "",
        show_alert: false,
        alert_text: "",
        item_visibility_text: {1: "mdi-eye", 0: "mdi-eye-off"}
    },
    methods: {
        /**
         * Try submitting entry
         */
        submit_entry: function() {
            if (vue_admin.type === "") {
                this.alert_text = "Fill all entries"
                this.show_alert = true
            }
            axios.post(`/${vue_admin.type}s`, {
                "title": vue_admin.title,
                "description": vue_admin.description,
                "url": vue_admin.url,
                "image_url": vue_admin.image_url,
                "time_stamp": vue_admin.time_stamp,
            })
                .then(function(response) {
                    if (response.data["INFO"]) {
                        vue_admin.alert_text = response.data["INFO"]
                        vue_admin.show_alert = true
                    }
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
        /**
         * Get all repos and set this.projects and this.latest_project
         */
        get_repos: function() {
            // Get all public repos
            axios.get("/public_repos")
                .then(function(response) {
                    vue_admin.projects = response["data"]["repos"]
                    vue_admin.latest_project = vue_admin.projects[0]
                    vue_admin.updated = response["data"]["updated"]
                })
        },
        /**
         * Get all blogs and set this.blogs
         */
        get_blogs: function() {
            // Get all blogs
            axios.get("/blogs")
                .then(function(response) {
                    vue_admin.blogs = response["data"]["blogs"]
                })
        },
        /**
         * Get all publications and set this.publications
         */
        get_publications: function() {
            // Get all publications
            axios.get("/publications")
                .then(function(response) {
                    vue_admin.publications = response["data"]["publications"]
                })
        },
        /**
         * Send a POST request to update visibility
         * @param projects, list of projects to update
         */
        send_selection: function (projects) {
            if (projects === []) {
                this.alert_text = "Nothing selected"
                this.show_alert = true
            }
            axios.post("public_repos", {
                "projects": projects
            })
                .then(function(response) {
                    if (response.data["INFO"]) {
                        vue_admin.alert_text = response.data["INFO"]
                        vue_admin.show_alert = true
                    }
                })
        },
        /**
         * Toggle visibility of project and send a post request to the backend
         * @param item, project object
         */
        toggle_visibility: function (item) {
            if (item.visible === 1) {
                item.visible = 0
            } else {
                item.visible = 1
            }
            vue_admin.send_selection([item])
        }
    },
    created: function() {
        this.get_repos()
        this.get_blogs()
        this.get_publications()
    }
})