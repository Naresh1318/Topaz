let vue_admin = new Vue({
    el: "#app",
    vuetify: new Vuetify(),
    data: {
        types: ["blog", "publication"],
        title: "",
        description: "",
        url: "",
        image_url: "",
        time_stamp: "",
        type: "",
    },
    methods: {
        submit_entry: function() {
            axios.post(`/${vue_admin.type}s`, {
                "title": vue_admin.title,
                "description": vue_admin.description,
                "url": vue_admin.url,
                "image_url": vue_admin.image_url,
                "time_stamp": vue_admin.time_stamp
            })
                .then(function(response) {
                    if (response.data["INFO"] === `${vue_admin.type} added`) {
                        alert(`${vue_admin.type} added`)
                    }
                })
        },
    }
})